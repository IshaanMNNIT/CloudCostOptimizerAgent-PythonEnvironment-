from simulator.request_queue import RequestQueue
from simulator.vm_manager import VMManager

from simulator.traffic.normal import NormalTrafficGenerator
from simulator.traffic.burst import BurstTrafficGenerator
from simulator.traffic.anomaly import AnomalyTrafficGenerator

from simulator.network.latency import NetworkLatencyModel
from simulator.network.bandwidth import BandwidthModel

from simulator.failures.failure_engine import FailureEngine
from simulator.services.service_manager import ServiceManager


class CloudEnvironment:
    def __init__(self):
        self.queue = RequestQueue()
        self.vm_manager = VMManager()
        self.failure_engine = FailureEngine()

        self.normal_traffic = NormalTrafficGenerator()
        self.burst_traffic = BurstTrafficGenerator()
        self.anomaly_traffic = AnomalyTrafficGenerator()

        self.network_latency = NetworkLatencyModel()
        self.bandwidth_model = BandwidthModel()
        self.service_manager = ServiceManager()

        self.time_step = 0
        self.latency = 0
        self.base_latency = 0

        self.current_traffic = 0
        self.traffic_delta = 0

        self.is_bursting = False
        self.is_anomalous = False

        self.bandwidth_metrics = {}
        self.service_metrics = {}

        self.failed_this_step = {}
        self.recovered_this_step = {}

    def generate_traffic(self):
        # Normal traffic + trend
        traffic, self.traffic_delta = self.normal_traffic.generate(
            self.time_step
        )

        # Burst overlay
        traffic, self.is_bursting = self.burst_traffic.apply(
            traffic
        )

        # Anomaly overlay
        traffic, self.is_anomalous = self.anomaly_traffic.apply(
            traffic
        )

        return traffic

    def handle_action(self, action):
        action_map = {
            "scale_up_small": ("up", "small"),
            "scale_up_medium": ("up", "medium"),
            "scale_up_large": ("up", "large"),
            "scale_down_small": ("down", "small"),
            "scale_down_medium": ("down", "medium"),
            "scale_down_large": ("down", "large"),
        }

        if action not in action_map:
            return

        direction, vm_type = action_map[action]

        if direction == "up":
            self.vm_manager.scale_up(vm_type)
        else:
            self.vm_manager.scale_down(vm_type)

    def step(self, action=None):
        self.time_step += 1

        # Action handling
        self.handle_action(action)

        # Traffic generation
        self.current_traffic = self.generate_traffic()

        # Queue admission
        accepted, dropped = self.queue.add_requests(
            self.current_traffic
        )

        # Compute capacity
        total_capacity = self.vm_manager.get_total_capacity()

        # Failure injection
        self.failed_this_step = self.failure_engine.trigger_failures(
            self.vm_manager.active_vms
        )

        # Recovery update
        self.recovered_this_step = self.failure_engine.step()

        # Effective capacity after failures
        failed_capacity = (
            self.failure_engine.get_state()["total_failed_vms"] * 100
        )

        effective_capacity = max(
            1,
            total_capacity - failed_capacity
        )

        # Request servicing
        served = self.queue.serve_requests(
            effective_capacity
        )

        # Queue metrics update
        self.queue.update_metrics()

        # VM internal clock
        self.vm_manager.step()

        # Network congestion
        self.bandwidth_metrics = (
            self.bandwidth_model.compute_congestion_metrics(
                self.current_traffic
            )
        )

        # Base environment latency
        self.base_latency = self.network_latency.compute_latency(
            self.queue.queue_length,
            effective_capacity
        ) + self.bandwidth_metrics["congestion_penalty"]

        # Multi-service latency
        self.latency, self.service_metrics = (
            self.service_manager.compute_service_latencies(
                self.current_traffic,
                self.base_latency
            )
        )

        return self.get_state()

    def get_state(self):
        service_state = self.service_manager.get_state(
            self.current_traffic,
            self.base_latency
        )

        return {
            "time_step": self.time_step,

            # Traffic
            "current_traffic": self.current_traffic,
            "traffic_delta": self.traffic_delta,
            "is_bursting": self.is_bursting,
            "is_anomalous": self.is_anomalous,

            # Network
            **self.bandwidth_metrics,

            # Latency
            "base_latency": self.base_latency,
            "total_latency": self.latency,

            # Failures
            **self.failure_engine.get_state(),

            # Services
            **service_state,

            # Queue
            **self.queue.get_state(),

            # Compute
            **self.vm_manager.get_state(),
        }
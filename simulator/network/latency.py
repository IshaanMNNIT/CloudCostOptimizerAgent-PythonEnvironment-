import random

class NetworkLatencyModel:
    def __init__(self, base_latency=20, jitter_factor=0.05):
        self.base_latency = base_latency
        self.jitter_factor = jitter_factor # Real-world network noise

    def compute_latency(self, queue_length, capacity):
        """
        Theory: Combined Queuing Delay + Network Jitter.
        """
        # Base queuing math
        queue_delay = (queue_length / max(1, capacity))
        
        # Add Network Jitter (White Noise)
        # Theory: Prevents the agent from over-fitting to a perfectly clean latency signal.
        jitter = random.uniform(-self.jitter_factor, self.jitter_factor) * self.base_latency
        
        total_latency = self.base_latency + queue_delay + jitter
        
        return max(self.base_latency, total_latency)
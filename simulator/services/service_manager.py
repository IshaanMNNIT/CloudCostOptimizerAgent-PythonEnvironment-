class ServiceManager:
    def __init__(self):
        # We add 'Resource Sensitivity' to each service
        self.services = {
            "api": {
                "traffic_share": 1.0, 
                "latency_base": 1.0,
                "load_factor": 0.001 # How much extra latency per 1 unit of traffic
            },
            "db": {
                "traffic_share": 0.7, 
                "latency_base": 1.5,
                "load_factor": 0.005 # DBs are more sensitive to load than APIs
            },
            "cache": {
                "traffic_share": 0.4, 
                "latency_base": 0.2,
                "load_factor": 0.0001 # Caches are very fast and stable
            }
        }

    def compute_service_latencies(self, total_traffic, base_env_latency):
        """
        Theory: Models 'Congestion Collapse' in specific microservices.
        """
        service_metrics = {}
        cumulative_system_latency = 0

        for name, config in self.services.items():
            service_traffic = total_traffic * config["traffic_share"]
            
            # Non-linear latency: base + (traffic * load_sensitivity)
            # Theory: Queuing theory predicts latency rises exponentially as we hit capacity
            s_latency = (base_env_latency * config["latency_base"]) + \
                        (service_traffic * config["load_factor"])
            
            service_metrics[name] = {
                "traffic": int(service_traffic),
                "latency": s_latency
            }
            cumulative_system_latency += s_latency

        return cumulative_system_latency, service_metrics

    def get_state(self, total_traffic, base_env_latency):
        total_l, metrics = self.compute_service_latencies(total_traffic, base_env_latency)
        return {
            "total_system_latency": total_l,
            "db_load_ratio": metrics["db"]["traffic"] / 1000, # Example normalization
            "is_db_bottleneck": metrics["db"]["latency"] > metrics["api"]["latency"]
        }
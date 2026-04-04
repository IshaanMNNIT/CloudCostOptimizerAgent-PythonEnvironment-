class BandwidthModel:
    def __init__(self, max_bandwidth=1000, sensitivity=50):
        self.max_bandwidth = max_bandwidth
        self.sensitivity = sensitivity

    def compute_congestion_metrics(self, traffic):
        """
        Theory: Models 'Packet Drops' and 'Throttling' when bandwidth is exceeded.
        """
        utilization = traffic / self.max_bandwidth
        
        # Non-linear penalty: Congestion gets exponentially worse after 90%
        # Helps the agent learn to fear the limit before it hits it.
        if utilization > 0.9:
            penalty = (utilization ** 2) * self.sensitivity
        else:
            penalty = 0

        return {
            "bandwidth_utilization": min(utilization, 1.2), # Clipped for RL stability
            "congestion_penalty": penalty,
            "is_throttled": utilization > 1.0
        }
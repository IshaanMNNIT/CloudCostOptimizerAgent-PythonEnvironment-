class ThresholdPolicy:
    def predict(self, state):
        latency = state["total_latency"]
        queue = state["queue_length"]

        if latency > 120 or queue > 500:
            return 2

        if latency < 40 and queue < 50:
            return 4

        return 0
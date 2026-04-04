class HeuristicPolicy:
    def predict(self, state):
        latency = state["total_latency"]
        queue = state["queue_length"]
        delta = state["traffic_delta"]
        failed = state["total_failed_vms"]

        if failed > 0:
            return 3

        if latency > 150:
            return 3

        if queue > 300 and delta > 0:
            return 2

        if latency < 50 and queue < 100:
            return 4

        return 0
class RewardFunction:
    def __init__(self, sla_target=100):
        self.w_latency = 2.0
        self.w_cost = 0.1
        self.w_drop = 5.0
        self.w_instability = 0.1
        self.w_recovery = 0.1
        self.sla_target = sla_target

    def compute(self, state, action=None):
        reward = 0.0

        latency_ratio = state["total_latency"] / self.sla_target

        if latency_ratio > 1.0:
            reward -= self.w_latency * (latency_ratio ** 2)

        reward -= self.w_cost * (
            state["total_hourly_cost"] / 50.0
        )

        drop_impact = min(
            state["dropped_requests"] / 100.0,
            10.0
        )
        reward -= self.w_drop * drop_impact

        if (
            state["queue_length"] == 0
            and state["total_latency"] < self.sla_target
        ):
            reward += 0.5

        if state["queue_delta"] < 0:
            reward += self.w_recovery * (
                abs(state["queue_delta"]) / 1000.0
            )

        if (
            action == 0
            and state["total_latency"] > self.sla_target
        ):
            reward -= 2.0

        if action is not None and action != 0:
            reward -= self.w_instability

        return reward
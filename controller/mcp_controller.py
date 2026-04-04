from stable_baselines3 import PPO


class MCPController:
    def __init__(self, env, model_path):
        self.env = env
        self.model = PPO.load(model_path, device="cpu")

    def observe(self):
        return self.env.env.get_state()

    def decide(self, obs):
        action, _ = self.model.predict(
            obs,
            deterministic=True
        )
        return int(action)

    def fallback_policy(self, state):
        latency = state["total_latency"]
        queue = state["queue_length"]

        if latency > 200 or queue > 2000:
            return 3   # SCALE_UP_LARGE

        if latency > 120 or queue > 1000:
            return 2   # SCALE_UP_MEDIUM

        if (
            latency < 40
            and queue < 10
            and state["cooldown_remaining"] == 0
        ):
            return 5   # SCALE_DOWN_MEDIUM

        return 0       # NO_OP

    def override_if_needed(self, action, state):
        latency = state["total_latency"]

        # Proactive burst protection
        if state["is_bursting"] and action == 0:
            return 1   # SCALE_UP_SMALL

        # Non-responsive agent protection
        if latency > 100 and action in [0, 4, 5, 6]:
            return self.fallback_policy(state)

        return action

    def execute(self, action):
        return self.env.step(action)

    def step(self, obs):
        state = self.observe()

        proposed_action = self.decide(obs)

        final_action = self.override_if_needed(
            proposed_action,
            state
        )

        next_obs, reward, terminated, truncated, info = (
            self.execute(final_action)
        )

        return {
            "state": state,
            "proposed_action": proposed_action,
            "final_action": final_action,
            "override_triggered": (
                proposed_action != final_action
            ),
            "reward": reward,
            "next_obs": next_obs,
            "terminated": terminated,
            "truncated": truncated
        }
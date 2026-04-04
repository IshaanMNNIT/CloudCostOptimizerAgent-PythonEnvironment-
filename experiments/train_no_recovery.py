from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv
from reward_function import RewardFunction


class NoRecoveryReward(RewardFunction):
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

        if (
            action == 0
            and state["total_latency"] > self.sla_target
        ):
            reward -= 2.0

        if action is not None and action != 0:
            reward -= self.w_instability

        return reward


env = CloudGymEnv()
env.reward_fn = NoRecoveryReward()

model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    gamma=0.95,
    n_steps=512,
    batch_size=64,
    ent_coef=0.01,
    verbose=1,
    device="cpu"
)

model.learn(total_timesteps=100000)
model.save("models/ppo_no_recovery")
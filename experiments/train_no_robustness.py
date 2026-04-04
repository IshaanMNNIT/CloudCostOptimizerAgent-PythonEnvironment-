from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv
from state_encoder import StateEncoder
import numpy as np


class NoRobustEncoder(StateEncoder):
    def encode(self, state):
        x = super().encode(state).copy()

        x[3] = 0.0
        x[11] = 0.0
        x[12] = 0.0

        return x.astype(np.float32)


env = CloudGymEnv()
env.encoder = NoRobustEncoder()

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
model.save("models/ppo_no_robustness")
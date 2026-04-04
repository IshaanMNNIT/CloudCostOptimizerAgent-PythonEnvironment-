import gymnasium as gym
from gymnasium import spaces
import numpy as np

from simulator.cloud_env import CloudEnvironment
from state_encoder import StateEncoder
from reward_function import RewardFunction


class CloudGymEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.env = CloudEnvironment()
        self.encoder = StateEncoder()
        self.reward_fn = RewardFunction()

        self.action_space = spaces.Discrete(7)

        self.observation_space = spaces.Box(
            low=-2,
            high=2,
            shape=(21,),
            dtype=np.float32
        )

        self.action_map = {
            0: None,
            1: "scale_up_small",
            2: "scale_up_medium",
            3: "scale_up_large",
            4: "scale_down_small",
            5: "scale_down_medium",
            6: "scale_down_large",
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.env = CloudEnvironment()

        # Prime state using one no-op step
        state = self.env.step(None)

        obs = self.encoder.encode(state)

        return obs, {}

    def step(self, action):
        if isinstance(action, (list, tuple)):
            action = action[0]

        if hasattr(action, "item"):
            action = action.item()

        action_name = self.action_map[action]

        state = self.env.step(action_name)

        reward = self.reward_fn.compute(
            state,
            action
        )

        override_penalty = 0.0

        if (
            state["total_latency"] > 100
            and action == 0
        ):
            override_penalty = -2.0

        reward += override_penalty

        obs = self.encoder.encode(state)

        terminated = False
        truncated = self.env.time_step >= 288

        return obs, reward, terminated, truncated, {}
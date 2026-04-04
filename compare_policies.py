import random
import numpy as np

from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv

from policies.static_policy import StaticPolicy
from policies.threshold_policy import ThresholdPolicy
from policies.heuristic_policy import HeuristicPolicy


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)


def evaluate_baseline(policy, steps=288, seed=42):
    set_seed(seed)

    env = CloudGymEnv()
    obs, _ = env.reset()

    total_reward = 0

    for _ in range(steps):
        raw_state = env.env.get_state()
        action = policy.predict(raw_state)

        obs, reward, terminated, truncated, _ = env.step(action)

        total_reward += reward

        if terminated or truncated:
            break

    return total_reward


def evaluate_ppo(steps=288, seed=42):
    set_seed(seed)

    env = CloudGymEnv()
    model = PPO.load(
        "models/ppo_v2_final",
        device="cpu"
    )

    obs, _ = env.reset()
    total_reward = 0

    for _ in range(steps):
        action, _ = model.predict(
            obs,
            deterministic=True
        )

        obs, reward, terminated, truncated, _ = env.step(action)

        total_reward += reward

        if terminated or truncated:
            break

    return total_reward


def run():
    results = {
        "Static": evaluate_baseline(
            StaticPolicy(),
            seed=42
        ),
        "Threshold": evaluate_baseline(
            ThresholdPolicy(),
            seed=42
        ),
        "Heuristic": evaluate_baseline(
            HeuristicPolicy(),
            seed=42
        ),
        "PPO": evaluate_ppo(
            seed=42
        ),
    }

    print("=" * 80)
    print("FAIR POLICY COMPARISON (SEEDED)")
    print("=" * 80)

    for name, score in results.items():
        print(f"{name:<15} | Reward: {score:.2f}")


if __name__ == "__main__":
    run()
import random
import numpy as np
from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)


def evaluate(model_path, seed=42):
    set_seed(seed)

    env = CloudGymEnv()
    model = PPO.load(model_path, device="cpu")

    obs, _ = env.reset()

    total_reward = 0

    for _ in range(288):
        action, _ = model.predict(obs, deterministic=True)

        obs, reward, terminated, truncated, _ = env.step(action)

        total_reward += reward

        if terminated or truncated:
            break

    return total_reward


def run():
    models = {
        "Full PPO": "models/ppo_v2_last_manual",
        "No Recovery": "models/ppo_no_recovery",
        "No Delta": "models/ppo_no_delta",
        "No Robustness": "models/ppo_no_robustness"
    }

    print("=" * 80)
    print("ABLATION STUDY")
    print("=" * 80)

    for name, path in models.items():
        score = evaluate(path)
        print(f"{name:<20} | Reward: {score:.2f}")


if __name__ == "__main__":
    run()
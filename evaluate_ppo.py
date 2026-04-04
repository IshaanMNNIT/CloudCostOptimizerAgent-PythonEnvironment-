from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv


def evaluate(steps=288):
    env = CloudGymEnv()
    model = PPO.load("models/ppo_v2_last_manual" , device="cpu")

    obs, _ = env.reset()

    total_reward = 0

    print("=" * 120)
    print("PPO POLICY EVALUATION")
    print("=" * 120)

    for step in range(steps):
        action, _ = model.predict(obs, deterministic=True)

        obs, reward, terminated, truncated, _ = env.step(action)

        total_reward += reward

        print(
            f"Step {step+1:03d} | "
            f"Action: {action} | "
            f"Reward: {reward:.2f}"
        )

        if terminated or truncated:
            break

    print("=" * 120)
    print(f"Total Reward: {total_reward:.2f}")


if __name__ == "__main__":
    evaluate()
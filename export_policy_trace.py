from gym_wrapper import CloudGymEnv
from stable_baselines3 import PPO


def export_trace():
    env = CloudGymEnv()
    obs, _ = env.reset()

    model = PPO.load(
        "models/ppo_v2_safe_tuned",
        device="cpu"
    )

    actions = []

    for _ in range(50):
        action, _ = model.predict(
            obs,
            deterministic=True
        )

        actions.append(int(action))

        obs, _, done, truncated, _ = env.step(action)

        if done or truncated:
            break

    with open("cloudsim_validation/actions.txt", "w") as f:
        for a in actions:
            f.write(f"{a}\n")


if __name__ == "__main__":
    export_trace()
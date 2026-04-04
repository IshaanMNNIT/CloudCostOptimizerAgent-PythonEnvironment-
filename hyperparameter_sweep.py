from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv


configs = [
    {"lr": 3e-4, "gamma": 0.99},
    {"lr": 1e-4, "gamma": 0.99},
    {"lr": 3e-4, "gamma": 0.95},
    {"lr": 1e-4, "gamma": 0.95},
]


def run_sweep():
    for i, config in enumerate(configs):
        print(f"\n=== RUN {i+1} ===")
        print(config)

        env = CloudGymEnv()

        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=config["lr"],
            gamma=config["gamma"],
            verbose=1,
            n_steps=512,
            batch_size=64,
            ent_coef=0.01,
            device="cpu"
        )

        model.learn(total_timesteps=5000)

        model.save(f"ppo_run_{i+1}")


if __name__ == "__main__":
    run_sweep()
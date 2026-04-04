from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from gym_wrapper import CloudGymEnv


def train():
    env = CloudGymEnv()

    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path="./models/",
        name_prefix="ppo_v2"
    )

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

    model.learn(
        total_timesteps=300000,
        callback=checkpoint_callback
    )

    model.save("models/ppo_v2_last_manual")
    print("Training complete. Model saved.")


if __name__ == "__main__":
    train()
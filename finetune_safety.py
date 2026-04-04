from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv
def finetune():

    env = CloudGymEnv()
    model = PPO.load(
    "models/ppo_v2_last_manual",
    env=env,
    device="cpu"
    )
    model.learn(total_timesteps=50000)
    model.save("models/ppo_v2_safe_tuned")

if __name__ == "__main__":
    finetune()
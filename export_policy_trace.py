import pandas as pd # Added for better logging
from gym_wrapper import CloudGymEnv
from stable_baselines3 import PPO
import os

def export_trace():
    os.makedirs("cloudsim_validation", exist_ok=True)
    os.makedirs("logs", exist_ok=True) # For Plot 5
    
    env = CloudGymEnv()
    obs, _ = env.reset(seed=42) # Consistent seed for validation

    model = PPO.load("models/ppo_v2_safe_tuned", device="cpu")

    actions = []
    
    # We increase this to 288 steps to match a full day for your plots
    for _ in range(288): 
        action, _ = model.predict(obs, deterministic=True)
        actions.append(int(action))
        obs, _, done, truncated, _ = env.step(action)
        if done or truncated:
            break

    # 1. Save for Java CloudSim Plus
    with open("cloudsim_validation/actions.txt", "w") as f:
        for a in actions:
            f.write(f"{a}\n")

    # 2. Save for Plot 5 (Action Frequency)
    action_df = pd.DataFrame({"action": actions})
    action_df.to_csv("logs/action_trace_logs.csv", index=False)

    print(f"Trace exported: 288 actions saved.")
    print(f"Action frequency data saved to logs/action_trace_logs.csv")

if __name__ == "__main__":
    export_trace()
import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv
import os
import random

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def evaluate_variant(model_path, num_episodes=10, steps=288):
    """Runs multiple episodes for a single model variant and returns the mean reward."""
    episode_rewards = []
    
    # We use a fresh environment for each variant
    env = CloudGymEnv()
    
    try:
        model = PPO.load(model_path, device="cpu")
    except Exception as e:
        print(f"Error loading {model_path}: {e}")
        return 0, 0

    for ep in range(num_episodes):
        # Ensure each variant faces the same sequence of 'random' challenges
        current_seed = 100 + ep 
        obs, _ = env.reset(seed=current_seed)
        set_seed(current_seed)
        
        total_reward = 0
        for _ in range(steps):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            if terminated or truncated:
                break
        
        episode_rewards.append(total_reward)

    return np.mean(episode_rewards), np.std(episode_rewards)

def run_study():
    os.makedirs("logs", exist_ok=True)
    
    # Your trained variants
    models = {
        "Full PPO": "models/ppo_v2_last_manual",
        "No Recovery": "models/ppo_no_recovery",
        "No Delta": "models/ppo_no_delta",
        "No Robustness": "models/ppo_no_robustness"
    }

    results = []

    print("=" * 80)
    print(f"{'Variant':<20} | {'Mean Reward':<15} | {'Std Dev':<10}")
    print("-" * 80)

    for name, path in models.items():
        # Running 10 episodes provides a 'Statistical Significance'
        mean_score, std_dev = evaluate_variant(path, num_episodes=10)
        
        print(f"{name:<20} | {mean_score:>15.2f} | {std_dev:>10.2f}")
        
        results.append({
            "Variant": name,
            "Mean_Reward": mean_score,
            "Std_Dev": std_dev
        })

    # Save to CSV for Plot 8
    df = pd.DataFrame(results)
    df.to_csv("logs/ablation_results.csv", index=False)
    
    print("=" * 80)
    print("Ablation data saved to 'logs/ablation_results.csv'")

if __name__ == "__main__":
    run_study()
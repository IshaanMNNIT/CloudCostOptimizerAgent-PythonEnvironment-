import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from gym_wrapper import CloudGymEnv
import os
import random

def set_seed(seed=42):
    """Sets the seed for reproducibility across all libraries."""
    random.seed(seed)
    np.random.seed(seed)
    # Note: Gymnasium environments often need their own seed in reset()
    return seed

def evaluate_multiple_runs(model_path="models/ppo_v2_last_manual", num_episodes=10, steps_per_episode=288):
    os.makedirs("logs", exist_ok=True)
    
    # Initialize the Environment
    env = CloudGymEnv()
    model = PPO.load(model_path, device="cpu")

    all_episode_data = []
    summary_stats = []

    print("=" * 120)
    print(f"STARTING MULTI-RUN EVALUATION: {num_episodes} Episodes")
    print("=" * 120)

    for episode in range(num_episodes):
        # We use a different seed for each episode to test diversity, 
        # but the sequence of seeds is predictable (42, 43, 44...)
        current_seed = 42 + episode
        obs, _ = env.reset(seed=current_seed)
        
        episode_reward = 0
        print(f"\nRunning Episode {episode + 1}/{num_episodes} (Seed: {current_seed})")

        for step in range(steps_per_episode):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)

            # Extract data for plotting
            state = env.env.get_state()
            state["episode"] = episode + 1
            state["step"] = step + 1
            state["reward"] = reward
            state["action"] = int(action)
            
            all_episode_data.append(state)
            episode_reward += reward

            if terminated or truncated:
                break
        
        summary_stats.append(episode_reward)
        print(f"Episode {episode + 1} Finished. Total Reward: {episode_reward:.2f}")

    # --- DATA EXPORT ---
    
    # 1. Detailed Logs (For Traffic vs Latency, Queue vs VM plots)
    full_df = pd.DataFrame(all_episode_data)
    full_df.to_csv("logs/ppo_detailed_eval.csv", index=False)

    # 2. Summary Logs (For Reward Histogram plot)
    summary_df = pd.DataFrame({"episode": range(1, num_episodes + 1), "total_reward": summary_stats})
    summary_df.to_csv("logs/ppo_summary_stats.csv", index=False)

    # --- FINAL REPORTING ---
    mean_r = np.mean(summary_stats)
    std_r = np.std(summary_stats)

    print("\n" + "=" * 120)
    print("FINAL EVALUATION RESULTS")
    print("=" * 120)
    print(f"Average Reward over {num_episodes} runs: {mean_r:.2f}")
    print(f"Standard Deviation: {std_r:.2f}")
    print(f"Best Run: {np.max(summary_stats):.2f} | Worst Run: {np.min(summary_stats):.2f}")
    print(f"Logs saved to 'logs/ppo_detailed_eval.csv'")
    print("=" * 120)

if __name__ == "__main__":
    # Recommended: Run 5-10 episodes to get a stable average for your plots
    evaluate_multiple_runs(num_episodes=10)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Setup
os.makedirs("plots", exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10})

def generate_all_plots():
    print("Generating report plots from actual logs...")

    # Load Data
    try:
        df_detailed = pd.read_csv("logs/ppo_detailed_eval.csv")
        df_summary = pd.read_csv("logs/ppo_summary_stats.csv")
        df_ablation = pd.read_csv("logs/ablation_results.csv")
        df_actions = pd.read_csv("logs/action_trace_logs.csv")
        df_cloudsim = pd.read_csv("cloudsim_validation/cloudsim_results.csv")
        java_latency = float(df_cloudsim.loc[df_cloudsim['metric'] == 'avg_finish_time', 'value'].values[0])
    except Exception as e:
        print(f"Error: {e}")
        return

    # 1. Traffic vs Latency
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    ax1.plot(df_detailed.index[:288], df_detailed['current_traffic'][:288], 'g-', alpha=0.5, label='Traffic')
    ax2.plot(df_detailed.index[:288], df_detailed['total_latency'][:288], 'b-', linewidth=1, label='Latency')
    ax1.set_ylabel('Traffic', color='g')
    ax2.set_ylabel('Latency (ms)', color='b')
    plt.title('Traffic vs Latency Response')
    plt.savefig("plots/1_traffic_latency.png")
    plt.close()

    # 2. Queue vs VM Count
    plt.figure(figsize=(10, 5))
    total_vms = df_detailed['small_vms'] + df_detailed['medium_vms'] + df_detailed['large_vms']
    plt.fill_between(df_detailed.index[:288], df_detailed['queue_length'][:288], color="orange", alpha=0.3, label='Queue')
    plt.step(df_detailed.index[:288], total_vms[:288] * 10, where='post', color="red", label='VMs (x10)')
    plt.legend()
    plt.title('Queue Length vs Resource Allocation')
    plt.savefig("plots/2_queue_vm.png")
    plt.close()

    # 3. Cost vs Latency Scatter
    plt.figure(figsize=(8, 6))
    plt.scatter(df_detailed['total_hourly_cost'], df_detailed['total_latency'], c=df_detailed['reward'], cmap='viridis', alpha=0.5)
    plt.xlabel('Cost ($)')
    plt.ylabel('Latency (ms)')
    plt.colorbar(label='Reward')
    plt.title('Cost-Performance Tradeoff')
    plt.savefig("plots/3_cost_latency_scatter.png")
    plt.close()

    # 4. Reward Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df_summary['total_reward'], kde=True, color='purple')
    plt.title('Policy Stability: Reward Distribution')
    plt.savefig("plots/4_reward_histogram.png")
    plt.close()

    # 5. Action Frequency (FIXED Palette Warning)
    plt.figure(figsize=(8, 5))
    sns.countplot(x='action', data=df_actions, hue='action', palette='viridis', legend=False)
    plt.xticks(range(7), ['No-Op', 'S-Up', 'M-Up', 'L-Up', 'S-Down', 'M-Down', 'L-Down'])
    plt.title('Action Frequency')
    plt.savefig("plots/5_action_frequency.png")
    plt.close()

    # 6. Intervention Timeline
    if 'override_triggered' in df_detailed.columns:
        plt.figure(figsize=(10, 2))
        overrides = df_detailed[df_detailed['override_triggered'] == 1].index
        plt.vlines(overrides, 0, 1, colors='red', alpha=0.5)
        plt.title('MCP Safety Interventions')
        plt.yticks([])
        plt.savefig("plots/6_intervention_timeline.png")
        plt.close()

    # 7. Baseline Comparison
    baselines = {'Static': -14890, 'Threshold': -30, 'Heuristic': 9, 'PPO': df_summary['total_reward'].mean()}
    plt.figure(figsize=(8, 5))
    plt.bar(baselines.keys(), baselines.values(), color=['grey', 'blue', 'orange', 'green'])
    plt.axhline(0, color='black', lw=1)
    plt.title('Baseline Performance Comparison')
    plt.savefig("plots/7_baseline_comparison.png")
    plt.close()

    # 8. Ablation Study (FIXED ValueError)
    plt.figure(figsize=(8, 5))
    # Using plt.bar directly to handle the pre-calculated error bars (yerr)
    plt.bar(df_ablation['Variant'], df_ablation['Mean_Reward'], 
            yerr=df_ablation['Std_Dev'], capsize=5, color=sns.color_palette("magma", len(df_ablation)))
    plt.title('Ablation Study: Feature Importance')
    plt.ylabel('Mean Reward')
    plt.savefig("plots/8_ablation_study.png")
    plt.close()

    # 9. CloudSim vs Python
    python_val = df_detailed['total_latency'].mean()
    java_val_norm = (java_latency / 1e8) 
    plt.figure(figsize=(6, 6))
    plt.bar(['Python Sim', 'CloudSim Plus'], [python_val, java_val_norm], color=['blue', 'green'])
    plt.title('Cross-Framework Validation')
    plt.savefig("plots/9_validation.png")
    plt.close()

    print("Success: All 9 plots saved in /plots/")

if __name__ == "__main__":
    generate_all_plots()
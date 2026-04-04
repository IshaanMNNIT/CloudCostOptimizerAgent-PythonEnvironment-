import matplotlib.pyplot as plt
from gym_wrapper import CloudGymEnv
from controller.mcp_controller import MCPController


def run_dashboard():
    env = CloudGymEnv()
    obs, _ = env.reset()

    controller = MCPController(
        env,
        "models/ppo_v2_safe_tuned"
    )

    steps = []
    traffic = []
    latency = []
    rewards = []
    vm_count = []
    overrides = []

    total_override = 0

    for step in range(100):
        result = controller.step(obs)
        obs = result["next_obs"]

        state = result["state"]

        steps.append(step + 1)
        traffic.append(state["current_traffic"])
        latency.append(state["total_latency"])
        rewards.append(result["reward"])

        total_vms = (
            state["small_vms"]
            + state["medium_vms"]
            + state["large_vms"]
        )
        vm_count.append(total_vms)

        override = int(result["override_triggered"])
        overrides.append(override)
        total_override += override

        if result["terminated"] or result["truncated"]:
            break

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.plot(steps, traffic)
    plt.title("Traffic Trend")
    plt.xlabel("Step")
    plt.ylabel("Traffic")

    plt.subplot(2, 2, 2)
    plt.plot(steps, latency)
    plt.title("Latency Trend")
    plt.xlabel("Step")
    plt.ylabel("Latency")

    plt.subplot(2, 2, 3)
    plt.step(steps, vm_count)
    plt.title("VM Scaling Timeline")
    plt.xlabel("Step")
    plt.ylabel("VM Count")

    plt.subplot(2, 2, 4)
    plt.plot(steps, rewards)
    plt.title("Reward Trend")
    plt.xlabel("Step")
    plt.ylabel("Reward")

    plt.tight_layout()
    plt.savefig("dashboard_output.png")
    plt.show()

    ratio = total_override / len(steps)
    print(f"Intervention Ratio: {ratio:.2%}")


if __name__ == "__main__":
    run_dashboard()
from gym_wrapper import CloudGymEnv
from controller.mcp_controller import MCPController


def test():
    env = CloudGymEnv()
    obs, _ = env.reset()

    controller = MCPController(
        env,
        "models/ppo_v2_safe_tuned"
    )

    print("=" * 100)
    print("MCP CONTROLLER TEST")
    print("=" * 100)

    for step in range(30):
        result = controller.step(obs)

        obs = result["next_obs"]

        print(
            f"Step {step + 1:02d} | "
            f"P: {result['proposed_action']} | "
            f"F: {result['final_action']} | "
            f"Override: {result['override_triggered']} | "
            f"Reward: {result['reward']:.2f}"
        )

        if result["terminated"] or result["truncated"]:
            break

    print("=" * 100)


if __name__ == "__main__":
    test()
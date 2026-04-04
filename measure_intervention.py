from gym_wrapper import CloudGymEnv
from controller.mcp_controller import MCPController


def measure():
    env = CloudGymEnv()
    obs, _ = env.reset()

    controller = MCPController(
        env,
        "models/ppo_v2_safe_tuned"
    )

    overrides = 0
    total = 100

    for _ in range(total):
        result = controller.step(obs)
        obs = result["next_obs"]

        if result["override_triggered"]:
            overrides += 1

        if result["terminated"] or result["truncated"]:
            break

    ratio = overrides / total

    print(f"Overrides: {overrides}")
    print(f"Intervention Ratio: {ratio:.2%}")


if __name__ == "__main__":
    measure()
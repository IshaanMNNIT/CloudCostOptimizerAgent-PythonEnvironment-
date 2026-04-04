from simulator.cloud_env import CloudEnvironment
from policies.static_policy import StaticPolicy
from policies.threshold_policy import ThresholdPolicy
from policies.heuristic_policy import HeuristicPolicy
from reward_function import RewardFunction


def evaluate_policy(policy, steps=288):
    env = CloudEnvironment()
    reward_fn = RewardFunction()

    total_reward = 0

    state = env.step(None)

    for _ in range(steps):
        action = policy.predict(state)

        action_map = {
            0: None,
            1: "scale_up_small",
            2: "scale_up_medium",
            3: "scale_up_large",
            4: "scale_down_small",
            5: "scale_down_medium",
            6: "scale_down_large",
        }

        state = env.step(action_map[action])

        reward = reward_fn.compute(state, action)

        total_reward += reward

    return total_reward


def run():
    policies = {
        "Static": StaticPolicy(),
        "Threshold": ThresholdPolicy(),
        "Heuristic": HeuristicPolicy(),
    }

    print("=" * 80)
    print("BASELINE POLICY EVALUATION")
    print("=" * 80)

    for name, policy in policies.items():
        score = evaluate_policy(policy)
        print(f"{name:<15} | Total Reward: {score:.2f}")


if __name__ == "__main__":
    run()
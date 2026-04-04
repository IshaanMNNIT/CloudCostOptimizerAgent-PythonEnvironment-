from simulator.cloud_env import CloudEnvironment


def run_validation(steps=100):
    env = CloudEnvironment()

    total_latency = 0
    total_cost = 0
    max_queue = 0
    failure_events = 0

    for step in range(steps):
        action = None

        if step == 10:
            action = "scale_up_medium"
        elif step == 30:
            action = "scale_up_large"
        elif step == 60:
            action = "scale_down_small"

        state = env.step(action)

        total_latency += state["latency"]
        total_cost += state["cost"]
        max_queue = max(max_queue, state["queue_length"])
        failure_events += state["failed_vms"]

    avg_latency = total_latency / steps
    avg_cost = total_cost / steps

    print("=" * 60)
    print("FULL SIMULATOR VALIDATION REPORT")
    print("=" * 60)
    print(f"Simulation Steps      : {steps}")
    print(f"Average Latency       : {avg_latency:.2f}")
    print(f"Average Cost          : {avg_cost:.2f}")
    print(f"Maximum Queue Length  : {max_queue}")
    print(f"Failure Event Count   : {failure_events}")
    print("=" * 60)


if __name__ == "__main__":
    run_validation()
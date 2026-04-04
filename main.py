from simulator.cloud_env import CloudEnvironment


def choose_action(step):
    action_schedule = {
        5: "scale_up_medium",
        15: "scale_up_large",
        25: "scale_down_small",
        35: "scale_up_small",
        45: "scale_down_medium",
    }

    return action_schedule.get(step, None)


def run_simulation(steps=60):
    env = CloudEnvironment()

    print("=" * 180)
    print("V2 CLOUD COST OPTIMIZER | FULL DEBUG TEST HARNESS")
    print("=" * 180)

    for step in range(steps):
        action = choose_action(step)

        state = env.step(action)

        print(
            f"Step {state['time_step']:02d} | "
            f"Traffic: {state['current_traffic']:4d} | "
            f"ΔT: {state['traffic_delta']:4d} | "
            f"Burst: {str(state['is_bursting']):5} | "
            f"Anomaly: {str(state['is_anomalous']):5} | "
            f"Queue: {state['queue_length']:4d} | "
            f"ΔQ: {state['queue_delta']:4d} | "
            f"EMA: {state['ema_wait_time']:.1f} | "
            f"BW: {state['bandwidth_utilization']:.2f} | "
            f"Throttle: {str(state['is_throttled']):5} | "
            f"Latency: {state['total_latency']:.2f} | "
            f"DB Bottleneck: {str(state['is_db_bottleneck']):5} | "
            f"Failed: {state['total_failed_vms']} | "
            f"Degraded: {str(state['is_system_degraded']):5} | "
            f"Small: {state['small_vms']} | "
            f"Medium: {state['medium_vms']} | "
            f"Large: {state['large_vms']} | "
            f"PendingCap: {state['pending_capacity']} | "
            f"Cooldown: {state['cooldown_remaining']} | "
            f"Cost: {state['total_hourly_cost']} | "
            f"Action: {action}"
        )


if __name__ == "__main__":
    run_simulation()
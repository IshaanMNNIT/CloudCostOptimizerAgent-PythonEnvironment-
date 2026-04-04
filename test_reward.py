from simulator.cloud_env import CloudEnvironment
from reward_function import RewardFunction

def test_scenarios():
    env = CloudEnvironment()
    rf = RewardFunction(sla_target=100)
    
    print(f"{'Scenario':<20} | {'Latency':<8} | {'Cost':<5} | {'Reward':<8}")
    print("-" * 55)

    # Scenario 1: Perfect Health (Low Latency, No Drops)
    s1 = env.get_state()
    s1["total_latency"] = 40
    s1["total_hourly_cost"] = 4
    s1["dropped_requests"] = 0
    r1 = rf.compute(s1, action=None)
    print(f"{'Perfect Health':<20} | {40:<8} | {4:<5} | {r1:.2f}")

    # Scenario 2: SLA Breach (Latency > 100)
    s2 = s1.copy()
    s2["total_latency"] = 250
    r2 = rf.compute(s2, action=None)
    print(f"{'SLA Breach':<20} | {250:<8} | {4:<5} | {r2:.2f}")

    # Scenario 3: Massive Over-provisioning (Low Latency, High Cost)
    s3 = s1.copy()
    s3["total_latency"] = 10
    s3["total_hourly_cost"] = 50
    r3 = rf.compute(s3, action=None)
    print(f"{'Over-Provisioned':<20} | {10:<8} | {50:<5} | {r3:.2f}")

    # Scenario 4: Catastrophic Drop
    s4 = s2.copy()
    s4["dropped_requests"] = 500
    r4 = rf.compute(s4, action=None)
    print(f"{'Catastrophic Drop':<20} | {250:<8} | {4:<5} | {r4:.2f}")

test_scenarios()
import numpy as np

class StateEncoder:
    @staticmethod
    def state_dim():
        return 21
    def encode(self, state):
        # We use np.clip to ensure outliers (like massive bursts) 
        # don't break the Neural Network's logic.
        return np.array([
            # --- Traffic (Normalized to ~0.0 - 1.0) ---
            np.clip(state["current_traffic"] / 1200, 0, 1.5),
            np.clip(state["traffic_delta"] / 500, -1, 1), # Delta can be negative!
            float(state["is_bursting"]),
            float(state["is_anomalous"]),

            # --- Queue (Logarithmic scaling is often better for big ranges) ---
            np.clip(state["queue_length"] / 5000, 0, 2.0),
            np.clip(state["queue_delta"] / 1000, -1, 1),
            np.clip(state["ema_wait_time"] / 5000, 0, 2.0),
            np.clip(state["dropped_requests"] / 500, 0, 1.0),

            # --- Network & Latency ---
            np.clip(state["bandwidth_utilization"], 0, 1.5),
            float(state["is_throttled"]),
            np.clip(state["total_latency"] / 200, 0, 2.0), # 2.0 means 400ms (Severe SLA breach)

            # --- Failures & Services ---
            np.clip(state["total_failed_vms"] / 5, 0, 1.0),
            float(state["is_system_degraded"]),
            np.clip(state["db_load_ratio"], 0, 1.0),
            float(state["is_db_bottleneck"]),

            # --- Compute & Efficiency ---
            np.clip(state["small_vms"] / 10, 0, 1.0),
            np.clip(state["medium_vms"] / 5, 0, 1.0),
            np.clip(state["large_vms"] / 3, 0, 1.0),
            np.clip(state["pending_capacity"] / 1500, 0, 1.0),
            state["cooldown_remaining"] / 5.0, # Exact range [0, 1]
            np.clip(state["total_hourly_cost"] / 50, 0, 1.0)
            
        ], dtype=np.float32)
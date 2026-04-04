import math
import random

class NormalTrafficGenerator:
    def __init__(self, base_load=200, amplitude=100, period=144, noise_level=0.1):
        self.base_load = base_load
        self.amplitude = amplitude
        self.period = period
        self.noise_level = noise_level # Percentage of noise (e.g., 10%)
        self.prev_load = base_load

    def generate(self, time_step):
        # 1. Base Sine Wave
        sine_val = math.sin(2 * math.pi * time_step / self.period)
        base_load = self.base_load + self.amplitude * sine_val

        # 2. Add Gaussian Noise (Real-world jitter)
        # Theory: Prevents the agent from perfectly memorizing the curve (Overfitting)
        noise = random.gauss(0, self.noise_level * self.amplitude)
        
        load = base_load + noise

        # 3. Calculate Traffic Delta (Velocity)
        # Theory: Essential for the 'queue_delta' we added to the RequestQueue
        traffic_delta = int(load) - self.prev_load
        self.prev_load = int(load)

        return max(0, int(load)), traffic_delta

    def get_state(self, time_step):
        """
        Theory: Provides the 'Phase' of the traffic to the agent.
        """
        return {
            "traffic_phase": (time_step % self.period) / self.period,
            "is_rising": math.cos(2 * math.pi * time_step / self.period) > 0
        }
import random

class BurstTrafficGenerator:
    def __init__(self, burst_probability=0.05, burst_multiplier=2.5, burst_duration=5):
        self.burst_probability = burst_probability
        self.burst_multiplier = burst_multiplier
        self.burst_duration = burst_duration
        self.remaining_burst_steps = 0

    def apply(self, traffic):
        is_bursting = False
        
        # 1. Continue existing burst
        if self.remaining_burst_steps > 0:
            self.remaining_burst_steps -= 1
            is_bursting = True
            return int(traffic * self.burst_multiplier), is_bursting

        # 2. Chance to trigger new burst
        # Theory: Models a 'Poisson Process' for incident arrival
        if random.random() < self.burst_probability:
            self.remaining_burst_steps = self.burst_duration - 1 # -1 because we apply now
            is_bursting = True
            return int(traffic * self.burst_multiplier), is_bursting

        return traffic, is_bursting
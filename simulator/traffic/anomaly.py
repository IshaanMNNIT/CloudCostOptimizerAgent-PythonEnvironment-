import random

class AnomalyTrafficGenerator:
    def __init__(self, anomaly_probability=0.02, spike_range=(400, 800), anomaly_duration=3):
        self.anomaly_probability = anomaly_probability
        self.spike_range = spike_range
        self.anomaly_duration = anomaly_duration
        self.remaining_anomaly_steps = 0
        self.current_spike = 0

    def apply(self, traffic):
        is_anomalous = False
        
        if self.remaining_anomaly_steps > 0:
            self.remaining_anomaly_steps -= 1
            is_anomalous = True
            return traffic + self.current_spike, is_anomalous

        if random.random() < self.anomaly_probability:
            self.current_spike = random.randint(*self.spike_range)
            self.remaining_anomaly_steps = self.anomaly_duration - 1
            is_anomalous = True
            return traffic + self.current_spike, is_anomalous

        return traffic, is_anomalous
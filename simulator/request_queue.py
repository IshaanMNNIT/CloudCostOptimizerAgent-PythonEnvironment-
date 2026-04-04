from collections import deque

class RequestQueue:
    def __init__(self, max_queue_size=10000, window_size=5, ema_alpha=0.3):
        self.queue_length = 0
        self.prev_queue_length = 0
        self.max_queue_size = max_queue_size
        self.dropped_requests = 0

        # EMA (Exponential Moving Average) for smoother RL signals
        self.ema_alpha = ema_alpha
        self.current_ema_wait = 0
        self.queue_delta = 0
        # Sliding window for raw statistics
        self.window_size = window_size
        self.wait_history = deque(maxlen=window_size)

    def add_requests(self, incoming_requests):
        """
        Logic: Finite Buffer Admission.
        Theory: Models 'Load Shedding' in high-traffic systems.
        """
        available_space = self.max_queue_size - self.queue_length
        accepted = min(incoming_requests, available_space)
        dropped = incoming_requests - accepted

        self.queue_length += accepted
        self.dropped_requests += dropped

        return accepted, dropped

    def serve_requests(self, capacity):
        """
        Logic: Service Rate Execution.
        Theory: Decouples demand from processing power.
        """
        served = min(self.queue_length, capacity)
        self.queue_length -= served
        return served

    def update_metrics(self):
        """
        Calculates the 'Velocity' and 'EMA' of the queue.
        Theory: Provides the agent with 'Acceleration' data to prevent SLA breaches.
        """
        # Calculate Delta (Velocity)
        self.queue_delta = self.queue_length - self.prev_queue_length
        self.prev_queue_length = self.queue_length

        # Update Sliding Window
        self.wait_history.append(self.queue_length)

        # Update EMA (Exponential Moving Average)
        # Formula: EMA_t = (Alpha * Current) + ((1 - Alpha) * EMA_t-1)
        self.current_ema_wait = (self.ema_alpha * self.queue_length) + \
                                ((1 - self.ema_alpha) * self.current_ema_wait)
        
        return self.queue_delta

    def get_avg_wait_time(self):
        if len(self.wait_history) == 0:
            return 0
        return sum(self.wait_history) / len(self.wait_history)

    def get_state(self):
        """
        Theory: Returns the Observation Vector O_t.
        Included Delta and EMA to solve 'State Aliasing' problems.
        """
        return {
            "queue_length": self.queue_length,
            "queue_delta": self.queue_delta,
            "avg_wait_time": self.get_avg_wait_time(),
            "ema_wait_time": self.current_ema_wait,
            "dropped_requests": self.dropped_requests
        }
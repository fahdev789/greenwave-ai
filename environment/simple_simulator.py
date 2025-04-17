import numpy as np

class TrafficSimulator:
    def __init__(self, arrival_rates, green_duration=10, max_queue=20):
        self.arrival_rates = arrival_rates  # dict: {'N': 0.3, 'S': 0.2, 'E': 0.5, 'W': 0.4}
        self.queues = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.green_direction = 'NS'  # or 'EW'
        self.green_duration = green_duration
        self.time = 0
        self.max_queue = max_queue

    def step(self):
        for dir in self.queues:
            if np.random.rand() < self.arrival_rates[dir]:
                self.queues[dir] = min(self.queues[dir] + 1, self.max_queue)

        if self.green_direction == 'NS':
            for dir in ['N', 'S']:
                self.queues[dir] = max(self.queues[dir] - 1, 0)
        else:
            for dir in ['E', 'W']:
                self.queues[dir] = max(self.queues[dir] - 1, 0)

        self.time += 1

    def switch_light(self):
        self.green_direction = 'EW' if self.green_direction == 'NS' else 'NS'

    def get_state(self):
        return dict(self.queues)

    def reset(self):
        self.queues = {k: 0 for k in self.queues}
        self.green_direction = 'NS'
        self.time = 0
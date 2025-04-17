import gymnasium as gym
from gymnasium import spaces
import numpy as np
from .simple_simulator import TrafficSimulator

class TrafficEnv(gym.Env):
    def __init__(self):
        super(TrafficEnv, self).__init__()
        self.sim = TrafficSimulator({"N": 0.3, "S": 0.2, "E": 0.4, "W": 0.5})
        self.action_space = spaces.Discrete(2)  # 0 = NS green, 1 = EW green
        self.observation_space = spaces.Box(low=0, high=self.sim.max_queue, shape=(4,), dtype=np.int32)

    def reset(self, seed=None, options=None):
        self.sim.reset()
        return self._get_obs(), {}

    def step(self, action):
        if action == 0:
            self.sim.green_direction = "NS"
        else:
            self.sim.green_direction = "EW"

        self.sim.step()
        obs = self._get_obs()
        reward = float(-sum(obs))  # Ensure reward is a float
        terminated = False
        truncated = self.sim.time >= 100
        return obs, reward, terminated, truncated, {}

    def _get_obs(self):
        q = self.sim.get_state()
        return np.array([q['N'], q['S'], q['E'], q['W']])

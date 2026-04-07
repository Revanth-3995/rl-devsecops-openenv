import gymnasium as gym
from gymnasium import spaces
import random

class DevSecOpsEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.actions = ["DETECT", "REPORT", "BLOCK", "PATCH", "ESCALATE", "APPROVE", "ROLLBACK"]
        self.action_space = spaces.Discrete(len(self.actions))

        self.observation_space = spaces.Dict({
            "task": spaces.Discrete(3),
            "severity": spaces.Box(low=0, high=10, shape=(1,))
        })

        self.state = {
            "task": 0,
            "severity": 5.0
        }

    def reset(self, seed=None, options=None):
        self.state = {
            "task": random.randint(0, 2),
            "severity": float(random.randint(1, 10))   # ✅ FIXED
        }
        return self.state, {}

    def step(self, action):
        action_name = self.actions[action]
        severity = self.state["severity"]

        # ✅ smarter reward logic
        if severity >= 7 and action_name in ["BLOCK", "ESCALATE"]:
            reward = 1.0
        elif severity >= 4 and action_name in ["PATCH", "DETECT"]:
            reward = 0.7
        elif action_name == "APPROVE" and severity <= 3:
            reward = 0.8
        else:
            reward = 0.2

        return self.state, float(reward), True, False, {}
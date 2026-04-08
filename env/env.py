import os
import random
import json
import gymnasium as gym
from gymnasium import spaces

from env.models import Observation
from env.tasks import get_random_task
from env.graders import clamp_score

class DevSecOpsEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.actions = ["DETECT", "REPORT", "BLOCK", "PATCH", "ESCALATE", "APPROVE", "ROLLBACK"]
        self.action_space = spaces.Discrete(len(self.actions))
        
        self.observation_space = spaces.Dict({
            "task": spaces.Discrete(3),
            "severity": spaces.Box(low=1.0, high=10.0, shape=(1,)),
            "cvss_base": spaces.Box(low=0.0, high=10.0, shape=(1,)),
            "cvss_temporal": spaces.Box(low=0.0, high=10.0, shape=(1,)),
            "cvss_environmental": spaces.Box(low=0.0, high=10.0, shape=(1,))
        })
        
        self.cve_data = self._load_mock_cves()
        self.state_model = None

    def _load_mock_cves(self):
        return [
            {"id": "CVE-2023-1", "severity": 9.8, "base": 9.8, "temporal": 9.5, "environmental": 9.5},
            {"id": "CVE-2023-2", "severity": 4.5, "base": 4.3, "temporal": 4.3, "environmental": 4.3},
            {"id": "CVE-2023-3", "severity": 2.1, "base": 2.1, "temporal": 2.1, "environmental": 2.1},
            {"id": "CVE-2024-4", "severity": 7.5, "base": 7.5, "temporal": 7.3, "environmental": 7.0},
        ]

    def _get_obs_array(self, obs_dict):
        # Extracts dict into flat array for tensor logic if necessary
        return [
            float(obs_dict["task"]),
            float(obs_dict["severity"]),
            float(obs_dict["cvss_base"]),
            float(obs_dict["cvss_temporal"]),
            float(obs_dict["cvss_environmental"])
        ]

    def reset(self, seed=None, options=None):
        if seed is not None:
            random.seed(seed)
            
        cve = random.choice(self.cve_data)
        
        self.state_model = Observation(
            task=get_random_task(),
            severity=float(cve["severity"]),
            cvss_base=float(cve["base"]),
            cvss_temporal=float(cve["temporal"]),
            cvss_environmental=float(cve["environmental"])
        )
        
        return self.state_model.model_dump(), {}

    def step(self, action):
        if hasattr(action, "item"):
            action = action.item()

        action_name = self.actions[int(action)]
        severity = self.state_model.severity
        
        reward = 0.0

        if severity >= 7 and action_name in ["BLOCK", "ESCALATE"]:
            reward += 1.0
        elif severity >= 4 and action_name in ["PATCH", "DETECT"]:
            reward += 0.7
        elif severity <= 3 and action_name == "APPROVE":
            reward += 0.8
            
        if action_name in ["BLOCK", "ESCALATE"]:
            reward -= 0.1
        if severity < 3 and action_name == "BLOCK":
            reward -= 1.0
        if severity >= 9 and action_name in ["APPROVE", "PATCH"]:
            reward -= 5.0
            
        final_reward = clamp_score(reward)
        
        # In a generic setup, an episode stops or not. True for simplification.
        return self.state_model.model_dump(), float(final_reward), True, False, {}

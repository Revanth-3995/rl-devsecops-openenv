import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical

class ActorCritic(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        
        self.action_head = nn.Linear(64, act_dim)
        self.value_head = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        
        action_logits = self.action_head(x)
        value = self.value_head(x)
        
        return action_logits, value

    def sample(self, x):
        action_logits, _ = self.forward(x)
        probs = torch.softmax(action_logits, dim=-1)
        m = Categorical(probs)
        action = m.sample()
        return action.item(), m.log_prob(action)

import torch
import torch.optim as optim
from env.env import DevSecOpsEnv
from agent.policy import ActorCritic

def train():
    env = DevSecOpsEnv()
    obs_dim = 5
    act_dim = env.action_space.n
    
    policy = ActorCritic(obs_dim, act_dim)
    optimizer = optim.Adam(policy.parameters(), lr=1e-3)
    
    episodes = 20
    for ep in range(episodes):
        state_dict, _ = env.reset()
        state = env._get_obs_array(state_dict)
        state_tensor = torch.FloatTensor(state)
        
        action, log_prob = policy.sample(state_tensor)
        
        next_state_dict, reward, done, _, _ = env.step(action)
        
        _, value = policy(state_tensor)
        advantage = reward - value.item()
        
        actor_loss = -log_prob * advantage
        critic_loss = (value - reward).pow(2)
        loss = actor_loss + critic_loss
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        print(f"Episode {ep} | Reward: {reward}")
        
    torch.save(policy.state_dict(), "agent/policy.pt")
    print("Saved policy to agent/policy.pt")

if __name__ == "__main__":
    train()

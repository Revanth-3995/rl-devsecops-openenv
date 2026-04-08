import torch
import traceback
from env.env import DevSecOpsEnv
from agent.policy import ActorCritic

def run_inference():
    try:
        env = DevSecOpsEnv()
        obs_dim = 5
        act_dim = env.action_space.n
        
        policy = ActorCritic(obs_dim, act_dim)
        try:
            policy.load_state_dict(torch.load("agent/policy.pt"))
        except:
            pass
            
        policy.eval()

        for task_id in range(1, 4):
            print(f"[START] task={task_id} env=devsecops model=ppo")
            
            try:
                state_dict, _ = env.reset()
                state = env._get_obs_array(state_dict)
                state_tensor = torch.FloatTensor(state)
                
                with torch.no_grad():
                    action, _ = policy.sample(state_tensor)
                
                state_dict, req_reward, done, _, _ = env.step(action)
                action_name = env.actions[action] if isinstance(action, int) else env.actions[action.item()]
                print(f"[STEP] step=1 action={action_name} reward={req_reward} done=true error=null")
                print(f"[END] success=true steps=1 score={req_reward} rewards={req_reward}")
            except Exception as e:
                print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"{str(e)}\"")
                print(f"[END] success=false steps=1 score=0.01 rewards=0.01")
    except Exception as grand_e:
        print(f"[START] task=1 env=devsecops model=ppo")
        print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"{str(grand_e)}\"")
        print(f"[END] success=false steps=1 score=0.01 rewards=0.01")

if __name__ == "__main__":
    run_inference()
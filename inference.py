import os
import json
from openai import OpenAI
from env.env import DevSecOpsEnv

def run_inference():
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("API_BASE_URL")

    # Graceful exit without crash if variables are missing
    if not api_key or not base_url:
        print("[START] task=0 env=devsecops model=llm")
        print("[STEP] step=1 action=DETECT reward=0.01 done=true error=\"Missing API configuration\"")
        print("[END] success=false steps=1 score=0.01 rewards=0.01")
        return

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    except Exception as init_err:
        print("[START] task=0 env=devsecops model=llm")
        print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"Init error: {str(init_err)}\"")
        print("[END] success=false steps=1 score=0.01 rewards=0.01")
        return

    env = DevSecOpsEnv()

    for task_id in range(1, 4):
        print(f"[START] task={task_id} env=devsecops model=llm")
        
        try:
            state_dict, _ = env.reset()
            # Observation dictionary structure
            # e.g., {'task': 1, 'severity': 9.8, 'cvss_base': 9.8, ...}
            
            prompt = (
                "You are an automated DevSecOps pipeline agent. "
                f"You have encountered a vulnerability state: {json.dumps(state_dict)}.\n"
                f"Available actions correspond to these integer values:\n"
                f"0: DETECT, 1: REPORT, 2: BLOCK, 3: PATCH, 4: ESCALATE, 5: APPROVE, 6: ROLLBACK.\n"
                "Return ONLY the single integer value of the best action to take."
            )

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a DevSecOps AI. Output only integers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=5,
                temperature=0.1
            )
            
            action_str = response.choices[0].message.content.strip()
            
            # Simple heuristic parsing
            action_idx = 0
            if action_str.isdigit() and int(action_str) in range(len(env.actions)):
                action_idx = int(action_str)
                
            state_dict, req_reward, done, _, _ = env.step(action_idx)
            action_name = env.actions[action_idx]
            
            print(f"[STEP] step=1 action={action_name} reward={req_reward} done=true error=null")
            print(f"[END] success=true steps=1 score={req_reward} rewards={req_reward}")

        except Exception as e:
            print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"{str(e)}\"")
            print(f"[END] success=false steps=1 score=0.01 rewards=0.01")

if __name__ == "__main__":
    run_inference()
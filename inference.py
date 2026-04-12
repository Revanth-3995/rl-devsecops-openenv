import os
import json
from openai import OpenAI
from env.env import DevSecOpsEnv

def run_inference():
    # Fetch credentials matching the Hackathon Sample
    api_key = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
    base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    benchmark_name = "devsecops"

    # Tasks array matching openenv.yaml
    tasks = ["secret_scanning", "cve_triage", "pipeline_audit"]

    # Graceful exit without crash if variables are missing
    if not api_key or not base_url:
        for t in tasks:
            print(f"[START] task={t} env={benchmark_name} model={model_name}")
            print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"Missing API configuration\"")
            print(f"[END] success=false steps=1 score=0.010 rewards=0.01")
        return

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    except Exception as init_err:
        for t in tasks:
            print(f"[START] task={t} env={benchmark_name} model={model_name}")
            print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"Init error: {str(init_err)}\"")
            print(f"[END] success=false steps=1 score=0.010 rewards=0.01")
        return

    env = DevSecOpsEnv()

    for task_name in tasks:
        print(f"[START] task={task_name} env={benchmark_name} model={model_name}")
        
        try:
            state_dict, _ = env.reset()
            # The observation dictionary contains pipeline states
            
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
            
            # Simple heuristic parsing and fallback
            action_idx = 0
            if action_str.isdigit() and int(action_str) in range(len(env.actions)):
                action_idx = int(action_str)
                
            state_dict, req_reward, done, _, _ = env.step(action_idx)
            action_name = env.actions[action_idx]
            
            req_reward = float(req_reward)
            success = req_reward >= 0.7  # Basic threshold boolean for success
            
            print(f"[STEP] step=1 action={action_name} reward={req_reward:.2f} done=true error=null")
            print(f"[END] success={str(success).lower()} steps=1 score={req_reward:.3f} rewards={req_reward:.2f}")

        except Exception as e:
            print(f"[STEP] step=1 action=DETECT reward=0.01 done=true error=\"{str(e)[:50]}\"")
            print(f"[END] success=false steps=1 score=0.010 rewards=0.01")

if __name__ == "__main__":
    run_inference()
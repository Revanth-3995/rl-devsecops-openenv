from devsecops_env import DevSecOpsEnv

env = DevSecOpsEnv()

for task_id in range(1, 4):
    print(f"[START] task_id={task_id} model=dummy")

    state, _ = env.reset()

    action = 0  # DETECT
    state, reward, done, _, _ = env.step(action)

    print(f"[STEP] step=1 action=DETECT reward={reward}")
    print(f"[END] task_id={task_id} total_reward={reward}")
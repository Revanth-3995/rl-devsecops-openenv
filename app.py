from fastapi import FastAPI
from pydantic import BaseModel
from devsecops_env import DevSecOpsEnv

app = FastAPI()
env = DevSecOpsEnv()
state, _ = env.reset()

class ActionRequest(BaseModel):
    action: int

@app.post("/reset")
def reset():
    global state
    state, _ = env.reset()
    return {"state": state}

@app.post("/step")
def step(req: ActionRequest):
    global state
    state, reward, done, _, _ = env.step(req.action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def get_state():
    return {"state": state}
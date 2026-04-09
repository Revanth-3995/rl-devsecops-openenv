from fastapi import FastAPI, Request
from env.env import DevSecOpsEnv
from env.models import ActionRequest

app = FastAPI()
env = DevSecOpsEnv()
state, _ = env.reset()

@app.post("/reset")
async def reset(request: Request):
    body = await request.body()
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

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()

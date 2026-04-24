---
title: RL DevSecOps OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: server/app.py
pinned: false
---

# RL-Based DevSecOps OpenEnv

## 🚀 Overview
This project implements a **DevSecOps simulation environment** properly packaged for the **Meta PyTorch Hackathon x Scaler School of Technology**. It simulates a CI/CD pipeline where an agent dynamically performs security actions (detecting secrets, triaging vulnerabilities) based on continuous risk levels and CVSS scores.

It natively supports a dual-pronged AI architecture:
1. **PyTorch TorchRL (PPO)** architectures designed for offline local training, proving the environment is solvable and mathematically sound.
2. **OpenAI LiteLLM Proxies** integrated directly into the `inference.py` script, serving as a standardized benchmark to evaluate zero-shot frontier LLM reasoning capabilities in DevOps contexts.

---

## 🏗️ Architecture

```text
┌────────────────────────────┐
│   LiteLLM /  ActorCritic   │
└────────────┬───────────────┘
             │ action
             ▼
┌────────────────────────────┐
│   DevSecOps Gym Env        │
│ (task + CVSS state array)  │
└────────────┬───────────────┘
             │ reward + next state
             ▼
┌────────────────────────────┐
│   FastAPI Server (uvicorn) │
│  /reset  /step  /state     │
└────────────┬───────────────┘
             │ HTTP
             ▼
┌────────────────────────────┐
│ Hugging Face Space (Docker)│
└────────────────────────────┘
```

---

## 📂 Comprehensive Project Structure

### Environment (`env/`)
- `env.py`: Core Gymnasium environment, generating pipeline states and evaluating rewards bounded strictly by `[0.01, 0.99]`.
- `models.py`: Pydantic BaseModels (`ActionRequest`, `Observation`) to enforce strict API typing.
- `graders.py`: Clamping and bounding logic functions ensuring compliance with Hackathon constraints.
- `tasks.py`: Helpers for randomly generating DevSecOps task assignments (Secret Scanning, CVE Triage).

### API Server (`server/`)
- `app.py`: FastAPI application wrapping the Gym environment to expose HTTP hooks (`/reset`, `/step`, `/state`). Contains the `main()` uvicorn entry point.

### Agents (`agent/`)
- `policy.py`: PyTorch model architectures (`ActorCritic` classes).
- `policy.pt`: Serialized PyTorch weights from the baseline trained RL model.

### Tooling & Inference
- `inference.py`: Target validation script. Evaluates environment states using the injected Hackathon Proxy LLM (`API_BASE_URL` and `HF_TOKEN`) via the `openai` client.
- `train_ppo.py`: Dedicated script to offline-train the PPO PyTorch agent against the DevSecOps Gym.
- `validate-submission.sh`: Local script for executing OpenEnv structural validation tests.
- `openenv.yaml`: OpenEnv multi-mode operational metadata.
- `pyproject.toml` / `uv.lock`: Project packaging definitions for rigorous dependency mapping (including FastApi, Uvicorn, Torch, and OpenAI).
- `Dockerfile`: OpenEnv Hugging Face image instruction.

---

## 🧠 DevSecOps Tasks Implemented

### 1. Secret Scanning
- Detect exposed credentials or misconfigured keys in code branches.
- Actions: `DETECT`, `REPORT`, `APPROVE`

### 2. CVE Triage
- Analyze vulnerability severity via temporal and environmental heuristics.
- Actions: `BLOCK`, `PATCH`, `ESCALATE`, `APPROVE`

### 3. Pipeline Security Audit
- Multi-stage decision-making across CI deployment stages.
- Actions: `BLOCK`, `PATCH`, `ESCALATE`, `APPROVE`, `ROLLBACK`

---

## ⚙️ Action Space

```python
["DETECT", "REPORT", "BLOCK", "PATCH", "ESCALATE", "APPROVE", "ROLLBACK"]
```

---

## 📊 Observation Space
The environment tracks complex pipeline states by integrating mocked CVSS v3.1 vector calculations:

```json
{
  "task": "Discrete(3)",
  "severity": "Box(1.0-10.0)",
  "cvss_base": "Box(0.0-10.0)",
  "cvss_temporal": "Box(0.0-10.0)",
  "cvss_environmental": "Box(0.0-10.0)"
}
```

---

## 🛠️ Usage

### 1. Initializing Environment 
Use standard python virtual environments or `uv` to leverage the packaged `pyproject.toml`:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Running FastAPI Target Server
The server runs out of the modular structure utilizing `uvicorn`:
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 3. Zero-Shot LLM Benchmark Inference
Execute the inference script to evaluate an integrated LLM via the proxy endpoint:
```bash
//
```
*(Handles missing `HF_TOKEN` gracefully to align with OpenEnv failure-fast testing)*

### 4. Validating Structure Locally
Verify the environment packaging using the deployment checker:
```bash
bash validate-submission.sh
```

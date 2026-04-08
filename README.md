---
title: RL DevSecOps OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# RL-Based DevSecOps OpenEnv Environment

## 🚀 Overview
This project implements a **DevSecOps simulation environment** compatible with OpenEnv for reinforcement learning-based security decision-making.

It simulates a CI/CD pipeline where an agent performs security-related actions such as detecting secrets, triaging vulnerabilities, and making deployment decisions based on risk levels.

---

## 🏗️ Architecture

```text
┌────────────────────────────┐
│      RL Agent / Policy     │
└────────────┬───────────────┘
             │ action
             ▼
┌────────────────────────────┐
│   DevSecOps Gym Env        │
│ (task + severity state)    │
└────────────┬───────────────┘
             │ reward + next state
             ▼
┌────────────────────────────┐
│   FastAPI Server (app.py)  │
│  /reset  /step  /state     │
└────────────┬───────────────┘
             │ HTTP
             ▼
┌────────────────────────────┐
│ Hugging Face Space (Docker)│
└────────────────────────────┘
```

---

## 📂 Project Structure

- `devsecops_env.py`: Core Gymnasium environment defining state, actions, and rewards for the DevSecOps simulation.
- `app.py`: FastAPI application exposing the environment via HTTP endpoints (`/reset`, `/step`, `/state`).
- `inference.py`: Dummy inference script to demonstrate how an agent interacts with the environment.
- `openenv.yaml`: OpenEnv metadata specification.
- `Dockerfile`: Containerizes the FastAPI server for easy deployment (e.g., Hugging Face Spaces).

---

## 🧠 Tasks Implemented

### 1. Secret Scanning
- Detect exposed credentials in code
- Actions: `DETECT`, `REPORT`, `APPROVE`

### 2. CVE Triage
- Analyze vulnerability severity and prioritize fixes
- Actions: `BLOCK`, `PATCH`, `ESCALATE`, `APPROVE`

### 3. Pipeline Security Audit
- Multi-stage decision-making across pipeline stages
- Actions: `BLOCK`, `PATCH`, `ESCALATE`, `APPROVE`, `ROLLBACK`

---

## ⚙️ Action Space

```python
["DETECT", "REPORT", "BLOCK", "PATCH", "ESCALATE", "APPROVE", "ROLLBACK"]
```

---

## 📊 Observation Space

```json
{
  "task": "int (0–2)",
  "severity": "float (1–10)"
}
```

---

## 🛠️ Installation & Usage

### 1. Local Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Running FastAPI Server
The application exposes a REST API to interact with the environment:
```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```
**Endpoints:**
- `POST /reset`: Resets the environment state.
- `POST /step`: Takes an action (e.g., `{"action": 0}`) and returns the next state, reward, and done flag.
- `GET /state`: Retrieves the current state.

### 3. Running Dummy Inference
Test the environment locally using the dummy agent:
```bash
python inference.py
```

### 4. Docker Deployment
You can also run this environment via Docker:
```bash
docker build -t devsecops-env .
docker run -p 7860:7860 devsecops-env
```

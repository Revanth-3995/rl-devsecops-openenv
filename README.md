# RL-Based DevSecOps OpenEnv Environment

## 🚀 Overview
This project implements a **DevSecOps simulation environment** compatible with OpenEnv for reinforcement learning-based security decision-making.

It simulates a CI/CD pipeline where an agent performs security-related actions such as detecting secrets, triaging vulnerabilities, and making deployment decisions based on risk levels.

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

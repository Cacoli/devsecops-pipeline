# DevSecOps CI/CD Pipeline

![CI Pipeline](https://github.com/Cacoli/devsecops-pipeline/actions/workflows/pipeline.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?logo=docker)
![Security](https://img.shields.io/badge/Security-DevSecOps-red?logo=shield)

A fully automated DevSecOps pipeline that integrates security scanning at every stage of the software delivery lifecycle. Every `git push` to `main` triggers a sequence of automated security gates — catching vulnerabilities, secrets, and misconfigurations before they reach production.

---

## Pipeline Overview
| Stage | Tool | What it catches |
|---|---|---|
| Unit Tests | pytest | Functional regressions |
| Container Scan | Trivy | CVEs in Docker image & dependencies |
| Secret Scan | Gitleaks | Hardcoded API keys, passwords, tokens |
| Static Analysis | Semgrep | Insecure code patterns, OWASP Top 10 |
| Dynamic Analysis | OWASP ZAP | Runtime vulnerabilities, missing security headers |
| Alerting | Discord Webhook | Real-time pipeline status per commit |

---

## Tech Stack

- **App:** Python + Flask (REST API)
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **SAST:** Semgrep (`p/python`, `p/owasp-top-ten`)
- **DAST:** OWASP ZAP (baseline scan)
- **Container Scanning:** Trivy
- **Secret Scanning:** Gitleaks
- **Alerting:** Discord Webhook

---

## How It Works

### 1. Unit Tests
pytest runs against the Flask API to confirm functional correctness before any security scanning begins.

### 2. Docker Build
The application is packaged into a Docker container — the same artifact that would ship to production.

### 3. Trivy — Container Scanning
Trivy scans the Docker image for known CVEs in the base image and installed packages. The pipeline fails on any `CRITICAL` or `HIGH` severity finding.

### 4. Gitleaks — Secret Detection
Gitleaks scans the git history for accidentally committed credentials. Catches API keys, database passwords, and tokens before they become a breach.

### 5. Semgrep — Static Analysis
Semgrep analyzes source code without executing it, flagging insecure patterns against the OWASP Top 10 ruleset. No runtime environment needed.

### 6. OWASP ZAP — Dynamic Analysis
ZAP spins up the Flask app and actively probes it for runtime vulnerabilities — things static analysis cannot catch, such as missing security headers, server information leakage, and content security policy issues.

### 7. Discord Webhook Alert
After every pipeline run, a Discord alert is sent to the `devsecops-alerts` server with the commit SHA — giving real-time visibility into the security status of every push.

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker
- Git

### Run Locally

```bash
git clone https://github.com/Cacoli/devsecops-pipeline.git
cd devsecops-pipeline
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000`.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/users` | Returns list of users |
| POST | `/login` | Accepts `{"username": "..."}` |

---

## Secrets Configuration

Add the following to your GitHub repository secrets (`Settings → Secrets → Actions`):

| Secret | Description |
|---|---|
| `DISCORD_WEBHOOK_URL` | Discord webhook URL for pipeline alerts |

---

## Security Design Decisions

- **Trivy ignores** are tracked in `.trivyignore` with documented justifications
- The `host="0.0.0.0"` Flask binding is intentional for Docker networking and suppressed via `# nosemgrep` with an inline comment explaining why
- ZAP warnings on missing security headers are acknowledged — these would be enforced at the reverse proxy layer in a production deployment

---

## Project Structure
devsecops-pipeline/

├── app.py                        # Flask API

├── test_app.py                   # pytest test suite

├── Dockerfile                    # Container definition

├── requirements.txt              # Python dependencies

├── .trivyignore                  # Trivy finding suppressions

└── .github/

└── workflows/

└── pipeline.yml          # GitHub Actions pipeline

# CodeBench — Docker Sandbox Compiler

An online compiler for Python, C++ and JavaScript. The browser sends code to a FastAPI service, a Celery worker runs it inside a short-lived Docker container, and the result is returned to the editor.

## Features

- Monaco-based editor with language selection, themes and custom stdin
- Asynchronous execution: the API returns a task id immediately, the client polls for the result
- Isolation per run: a fresh container with `--network=none`, a 128 MB memory limit, half a CPU and a 10 second timeout
- Static checks for Python before execution (blocked imports such as `os`, `subprocess`, `socket` and calls to `eval` / `exec`)
- Output truncation for very large outputs
- Optional WebSocket channel backed by Redis Pub/Sub

## Architecture

```
Browser (React)  ──POST /execute──▶  FastAPI  ──task──▶  Redis  ──▶  Celery worker
       ▲                                │                               │
       └──────GET /result/{id}──────────┘                     docker run sandbox_<lang>
```

| Path | Purpose |
|---|---|
| `backend/main.py` | FastAPI app: `/execute`, `/result/{task_id}`, `/ws/{task_id}` |
| `backend/celery_worker.py` | Celery task that dispatches code to the right runner |
| `backend/compiles/` | Per-language runners and safety checks |
| `backend/sandbox/run_in_docker.py` | Starts a sandbox container with resource limits |
| `backend/sandbox/{Python,Cpp,JS}/` | Dockerfiles of the sandbox images |
| `frontend/` | React client (Create React App + Tailwind) |
| `landing.html` | Static landing page of the project |

## Running locally

Requirements: Docker with Docker Compose, Node.js 18+.

```bash
# Backend: API, worker, Redis and the three sandbox images
cd backend
docker compose build
docker compose up backend celery redis

# Frontend
cd ../frontend
cp .env.example .env        # REACT_APP_API_URL=http://localhost:8000
npm install
npm start                   # http://localhost:3000
```

The worker talks to the host Docker daemon through `/var/run/docker.sock` and writes code to `/tmp/codebench-sandbox`, which is mounted at the same path in the worker and on the host.

## Configuration

| Variable | Where | Default |
|---|---|---|
| `REDIS_URL` | backend, worker | `redis://localhost:6379` |
| `ALLOWED_ORIGINS` | backend | `http://localhost:3000` (comma-separated list) |
| `SANDBOX_TMP` | worker | system temp directory |
| `REACT_APP_API_URL` | frontend | `http://localhost:8000` |

## Security notes

Mounting the Docker socket gives the worker control over the host Docker daemon. Run the stack on a dedicated machine or VM, never next to other services. The Python import filter is a convenience check, not a security boundary; isolation comes from the container limits.

# Prototypes

The first iterations of the online compiler, written with Flask. They run user code directly on the host with `subprocess` and have no isolation, so they are kept for reference only. The production-oriented version is [`docker-sandbox`](../docker-sandbox).

| Path | Description |
|---|---|
| `Compiler/` | Flask + Socket.IO servers per language (`python.py`, `cpp.py`, `js.py`) with live output and interactive input |
| `CompilerProject/` | Single-page variant with a shared editor |
| `forPython/`, `forCPP/`, `forJS/` | Minimal per-language servers |
| `newdesig/` | Static redesign of the editor UI |
| `DynamicResultCode.py`, `main.js` | Early experiment with streaming output over Socket.IO |

## Running

```bash
pip install flask flask-socketio
cd Compiler
python python.py      # http://localhost:5003 (cpp.py: 5001, js.py: 5002)
```

Requires Python 3, `g++` and Node.js on the machine for C++ and JavaScript execution.

Do not deploy these servers publicly: submitted code runs with the permissions of the server process.

# Online Compiler

A collection of browser-based code execution environments, built and refined over several iterations. Each directory is a self-contained project with its own README, dependencies and run instructions.

| Project | What it is | Stack |
|---|---|---|
| [`docker-sandbox`](docker-sandbox) | Multi-language online compiler (Python, C++, JavaScript). Code runs in isolated Docker containers, jobs are queued through Celery and Redis. | React, Monaco Editor, FastAPI, Celery, Redis, Docker |
| [`webcontainer-ide`](webcontainer-ide) | In-browser IDE that runs a real Node.js environment through the WebContainer API: file explorer, editor, terminal and live preview. | Next.js, Monaco Editor, xterm.js, Zustand, WebContainer API |
| [`pocket-ide`](pocket-ide) | Self-hosted IDE server for phones and tablets. Gives a mobile-friendly editor, tmux terminal and port preview for a remote Linux machine or Codespace. | Node.js, Express, node-pty, WebSocket, Next.js (static UI) |
| [`mobile-web-ide`](mobile-web-ide) | Offline-first HTML/CSS/JS editor that works as an installable PWA, with live preview, a virtual terminal and ZIP import/export. | Vanilla JavaScript, CodeMirror 6, IndexedDB, Service Worker |
| [`prototypes`](prototypes) | The first versions: Flask servers that compile and run code with `subprocess`. Kept for history. | Python, Flask, CodeMirror |

## How the projects relate

The work started with simple Flask prototypes that executed code directly on the host. The next step was isolation and scale: `docker-sandbox` moves execution into short-lived Docker containers with CPU, memory and network limits and processes jobs asynchronously. `webcontainer-ide` and `mobile-web-ide` take the opposite approach and run everything in the browser, so no server is needed. `pocket-ide` covers the remaining case: full Linux tooling, controlled comfortably from a phone.

## Repository layout

```
online-compiler/
├── docker-sandbox/     FastAPI + Celery backend, React frontend
├── webcontainer-ide/   Next.js app
├── pocket-ide/         Node.js server with a Next.js UI in web/
├── mobile-web-ide/     Static PWA, no build step required
└── prototypes/         Early Flask experiments
```

The history of each project was preserved when the original repositories were merged into this one.

## License

[MIT](LICENSE) © Vadym Zelenko

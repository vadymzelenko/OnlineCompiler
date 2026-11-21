# PocketIDE

A self-hosted IDE server designed to be used from a phone. Run it on any Linux machine (a home server, a Raspberry Pi-class board or GitHub Codespaces) and open it in a mobile browser: you get a file tree, a code editor, persistent tmux terminals and a preview of any local port.

## Features

- Token-protected access (Bearer header or cookie), rate-limited API
- Code editor (CodeMirror 6) with syntax highlighting for JS, HTML, CSS, JSON and Python
- Real terminals through `node-pty` and tmux, so sessions survive reconnects
- Preview of local dev servers at `/proxy/<port>/`
- Live file tree updates (chokidar), file upload
- Keyboard-first navigation and an on-screen helper bar for mobile keyboards
- Installable as a PWA on iOS and Android
- Single-file workspace archives (`*.pocket.json.gz`) with per-file SHA-256, restorable in the IDE or on any machine with Node.js

## Installation

```bash
sudo apt-get install -y tmux build-essential python3
cp .env.example .env     # set AUTH_TOKEN, at least 16 characters
npm run setup            # installs dependencies and builds the UI into web/out
npm start                # http://localhost:8080
```

GitHub Codespaces: add `AUTH_TOKEN` as a Codespaces secret, run `npm start`, make port 8080 public in the Ports tab and open the link on the phone. On iPhone use Share, then Add to Home Screen.

## Configuration

| Variable | Description | Default |
|---|---|---|
| `AUTH_TOKEN` | Access token, required, minimum 16 characters | none |
| `PORT` | HTTP port | `8080` |
| `WORKSPACE_DIR` | Root directory shown in the IDE | `/workspaces` in Codespaces, otherwise `~/projects` |

## Preview

Apps opened through `/proxy/<port>/` must work under a relative base path. For Vite set `base: './'`.

## Keyboard shortcuts

| Keys | Action |
|---|---|
| `Alt+/` | Help |
| `Alt+1` / `Alt+2` / `Alt+3` | Switch tabs |
| `Alt+0` | Focus the file tree (arrows, Enter, Delete) |
| `Alt+Shift+M` | Arrow-key mouse cursor |
| `Alt+Shift+A` | Download the selected folder as an archive |

tmux prefix is `Ctrl+B` (there is a `^B` button on the toolbar). Split a window with `^B %` or `^B "`.

## Workspace archives

```bash
node pocket.js pack   .  backup.pocket.json.gz
node pocket.js list   backup.pocket.json.gz
node pocket.js unpack backup.pocket.json.gz ./workspace
```

Archives are gzip-compressed JSON: text files are stored as is, binary files as base64. `.git` and `node_modules` are skipped. Only `pocket.js` is needed to unpack an archive.

## Security

The server gives full shell access to the machine it runs on. Use a long random token, serve it over HTTPS and do not expose it on a machine that holds anything you cannot afford to lose.

# WebContainer IDE

A browser IDE that runs a real Node.js environment in the tab using the [WebContainer API](https://webcontainers.io). No backend executes user code: `npm install`, dev servers and shell commands all run client-side.

## Features

- File explorer with create, rename, delete and ZIP export of the whole project
- Monaco editor with tabs
- Interactive `jsh` terminal (xterm.js) connected to the container
- Live preview that picks up the dev server through the `server-ready` event
- Project state (files, empty folders, open tabs) persisted between reloads and re-mounted on start
- Responsive layout: resizable panels on desktop, tab navigation on mobile

## Getting started

```bash
npm install
npm run dev      # http://localhost:3000
```

WebContainers require cross-origin isolation. `next.config.mjs` sends the `Cross-Origin-Embedder-Policy: require-corp` and `Cross-Origin-Opener-Policy: same-origin` headers on every route; any hosting provider must keep them.

## Structure

| Path | Purpose |
|---|---|
| `components/ide/` | `IDE`, `FileExplorer`, `Editor`, `Terminal`, `Preview` |
| `hooks/useWebContainer.js` | Boots the container, mounts files, starts the dev server |
| `store/useWebContainerStore.js` | Zustand store: container status, files, tabs |
| `lib/fileTree.js` | Conversion between the WebContainer tree format and a flat path map |
| `lib/persistence.js` | Saving and restoring project state |

## Limitations

The container lives in browser memory. After a full page reload `node_modules` and running processes are gone, so the IDE re-installs dependencies on start. WebContainers work in Chromium-based browsers and recent Firefox and Safari versions.

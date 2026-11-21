# Mobile Web IDE

An offline-first editor for HTML, CSS and JavaScript projects that runs entirely in the browser and installs as a PWA. Built for writing small front-end projects on a phone.

## Features

- CodeMirror 6 editor with HTML, CSS and JavaScript highlighting, autocompletion and formatting
- Live preview: `index.html` is assembled with the project's CSS and JS files inlined
- Virtual terminal with `ls`, `cd`, `mkdir`, `touch`, `rm`, `cat`, `echo`, `mv`, `cp`, `tree`, `edit` and more
- Projects stored in IndexedDB; optional auto-sync to a folder on disk through the File System Access API (Chrome, Edge)
- ZIP import and export
- Works offline through a Service Worker cache
- Layout adapted for portrait and landscape phones and for on-screen keyboards

## Running

There is no build step. Serve the directory with any static server:

```bash
npx serve .
# or
python3 -m http.server 8000
```

The bundled CodeMirror build in `src/vendor/codemirror.js` is generated from `scripts/editor-entry.js` with any ES module bundler, for example:

```bash
npx esbuild scripts/editor-entry.js --bundle --format=esm --minify --outfile=src/vendor/codemirror.js
```

## Updating the offline cache

The Service Worker precaches the files listed in `sw.js`. After changing any of them, bump the cache version (`const V = 'webide-vNN'`), otherwise installed copies keep serving the old files.

## Structure

| File | Purpose |
|---|---|
| `src/main.js` | App wiring, tabs, shortcuts |
| `src/fs.js` | Virtual file system on top of IndexedDB |
| `src/fs-folder.js` | Sync to a local folder (File System Access API) |
| `src/editor.js` | CodeMirror setup |
| `src/preview.js` | Preview assembly and refresh |
| `src/terminal.js` | Terminal commands |
| `src/zip.js` | ZIP import and export |

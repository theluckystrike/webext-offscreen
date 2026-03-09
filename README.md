[![CI](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml/badge.svg)](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)

# webext-offscreen

Typed offscreen document creation and messaging for Chrome MV3 extensions — DOM parsing, audio, canvas, clipboard, and more. Part of [@zovo/webext](https://github.com/theluckystrike/webext).

## Why Offscreen Documents?

Chrome Manifest V3 removed access to the DOM from service workers. Background scripts can no longer directly:

- Parse HTML with `DOMParser`
- Work with `<canvas>` elements
- Play audio through HTML5 `<audio>`
- Access the clipboard via the Clipboard API
- Use Web Workers directly

**Offscreen documents** provide a solution — they create a temporary page context that runs alongside your service worker, giving you full DOM and window APIs back.

## Features

- **Typed API** — Full TypeScript support with inferred types
- **Helper Pattern** — Reusable `OffscreenHelper` for cleaner code
- **Message Routing** — Register handlers by message type
- **Async Support** — Both sync and async handlers work seamlessly
- **Singleton Management** — Automatic creation/deduplication
- **Auto-cleanup** — Close documents when done
- **All MV3 Reasons** — Support for `DOM_PARSER`, `AUDIO_PLAYBACK`, `CLIPBOARD`, `WORKERS`, and more

## Install

```bash
npm install @theluckystrike/webext-offscreen
```

Or with pnpm:

```bash
pnpm add @theluckystrike/webext-offscreen
```

## Quick Start

### 1. Service Worker (Background)

```typescript
import { ensureOffscreen, sendToOffscreen, createOffscreenHelper } from "webext-offscreen";

// Option 1: Direct API
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content",
});

const result = await sendToOffscreen("parse", { html: "<p>Hello</p>" });

// Option 2: Helper pattern (recommended)
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content",
});

await offscreen.ensure();
const data = await offscreen.send("parse", { html: "<p>Hello</p>" });
await offscreen.close();
```

### 2. Offscreen Document (`offscreen.html`)

```typescript
import { onOffscreenMessage, setupOffscreenListener } from "webext-offscreen";

onOffscreenMessage("parse", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return { text: doc.body.textContent };
});

// Async handlers work too
onOffscreenMessage("fetch", async (data) => {
  const response = await fetch(data.url);
  return response.json();
});

setupOffscreenListener();
```

## Use Cases

### DOM Parsing

Parse HTML or XML in your background script:

```typescript
// Background
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML for content extraction",
});

await offscreen.ensure();
const { text, links } = await offscreen.send("extract", {
  html: `<html><body><a href="/a">Link</a></body></html>`
});
```

```typescript
// Offscreen
onOffscreenMessage("extract", ({ html }) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");
  const links = Array.from(doc.querySelectorAll("a")).map(a => a.href);
  return { text: doc.body.textContent, links };
});
```

### Canvas Operations

Generate images or process graphics:

```typescript
// Background
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["CANVAS"],
  justification: "Generate preview images",
});

const blob = await offscreen.send("generate", { width: 200, height: 200 });
// Use blob in your extension
```

### Audio Playback

Play sounds from the background:

```typescript
// Background
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["AUDIO_PLAYBACK"],
  justification: "Play notification sounds",
});

await offscreen.send("play", { src: "/sounds/alert.mp3" });
```

### Clipboard Access

Read/write clipboard from background:

```typescript
// Background
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["CLIPBOARD"],
  justification: "Copy extracted data to clipboard",
});

await offscreen.send("copy", { text: "Hello, clipboard!" });
```

### Web Workers

Run compute-heavy tasks:

```typescript
// Background
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["WORKERS"],
  justification: "Process large dataset with Web Worker",
});

const result = await offscreen.send("process", { data: bigArray });
```

## API Reference

### Service Worker Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `ensureOffscreen(config)` | Create offscreen document if not exists | `Promise<void>` |
| `hasOffscreen()` | Check if offscreen document is active | `Promise<boolean>` |
| `closeOffscreen()` | Close offscreen document | `Promise<void>` |
| `sendToOffscreen(type, data)` | Send typed message to offscreen | `Promise<TOut>` |
| `createOffscreenHelper(config)` | Create a reusable helper object | `OffscreenHelper` |

### Offscreen Helper Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `ensure()` | Ensure document exists | `Promise<void>` |
| `close()` | Close the document | `Promise<void>` |
| `isActive()` | Check if document is active | `Promise<boolean>` |
| `send(type, data)` | Send message to document | `Promise<TOut>` |

### Offscreen Document Functions

| Function | Description |
|----------|-------------|
| `onOffscreenMessage(type, handler)` | Register a message handler |
| `setupOffscreenListener()` | Start listening for messages |
| `removeHandler(type)` | Remove a message handler |
| `clearHandlers()` | Remove all handlers |

### Offscreen Reasons

All Chrome MV3 reasons are supported:

```
TESTING | AUDIO_PLAYBACK | BLOBS | CLIPBOARD | DOM_PARSER
DOM_SCRAPING | GEOLOCATION | LOCAL_STORAGE | MATCH_MEDIA | WORKERS
```

## License

MIT

---

Built by [theluckystrike](https://github.com/theluckystrike) — [zovo.one](https://zovo.one)

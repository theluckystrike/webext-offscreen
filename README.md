[![CI](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml/badge.svg)](https://github.com/theluckystrike/webext-offscreen/actions)
[![npm](https://img.shields.io/npm/v/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)

# webext-offscreen

Typed offscreen document creation and messaging for Chrome MV3 extensions.

Part of the [@zovo/webext](https://github.com/theluckystrike/webext) ecosystem.

## Why Offscreen Documents?

Chrome MV3 extensions removed DOM access from service workers. This broke common extension patterns:

- **DOM Parsing** — No more `document.createElement()` in background scripts
- **Audio/Video Processing** — Media elements require a DOM environment
- **Canvas Operations** — Drawing and image manipulation needs a document
- **Clipboard Access** — Advanced clipboard operations need DOM APIs

Offscreen documents provide a hidden DOM environment for these tasks. This library makes them type-safe and easy to use.

## Features

- ✅ **Typed API** — Full TypeScript support with proper types
- ✅ **Auto-close** — Automatically close documents when done
- ✅ **Singleton Pattern** — Helper class for reusable offscreen management
- ✅ **Message Passing** — Type-safe communication between background and offscreen
- ✅ **All Reasons** — Support for all Chrome offscreen document reasons

## Install

```bash
npm install @theluckystrike/webext-offscreen
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

### 2. Offscreen Document

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

## Use Case Examples

### DOM Parsing

Parse HTML content in the background without external dependencies:

```typescript
// Background script
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Extract metadata from HTML",
});

await offscreen.ensure();
const metadata = await offscreen.send<{ html: string }, { title: string; links: string[] }>("parse", {
  html: documentContent,
});
await offscreen.close();

// In offscreen.html
onOffscreenMessage("parse", (data) => {
  const doc = new DOMParser().parseFromString(data.html, "text/html");
  const links = Array.from(doc.querySelectorAll("a")).map((a) => a.href);
  return { title: doc.title, links };
});

setupOffscreenListener();
```

### Audio Playback

Process audio files in the background:

```typescript
// Background script
const audioOffscreen = createOffscreenHelper({
  url: "audio.html",
  reasons: ["AUDIO_PLAYBACK"],
  justification: "Analyze audio files",
});

await audioOffscreen.ensure();
const analysis = await audioOffscreen.send("analyze", { audioData: buffer });
```

### Canvas Operations

Draw images or generate graphics:

```typescript
// Background script
const canvasOffscreen = createOffscreenHelper({
  url: "canvas.html",
  reasons: ["BLOBS"],
  justification: "Generate preview images",
});

await canvasOffscreen.ensure();
const blob = await canvasOffscreen.send<{ width: number; height: number; color: string }, Blob>(
  "generate",
  { width: 200, height: 200, color: "#ff0000" }
);
```

### Clipboard Operations

Advanced clipboard access from background:

```typescript
// Background script
const clipboardOffscreen = createOffscreenHelper({
  url: "clipboard.html",
  reasons: ["CLIPBOARD"],
  justification: "Read clipboard with formatting",
});

await clipboardOffscreen.ensure();
const clipboardData = await clipboardOffscreen.send("read", {});
```

## API Reference

### Service Worker Functions

| Function | Description |
|----------|-------------|
| `ensureOffscreen(config)` | Create offscreen document if not exists |
| `hasOffscreen()` | Check if offscreen document is active |
| `closeOffscreen()` | Close offscreen document |
| `sendToOffscreen(type, data)` | Send typed message to offscreen document |
| `createOffscreenHelper(config)` | Create a reusable helper object |

### Offscreen Document Functions

| Function | Description |
|----------|-------------|
| `onOffscreenMessage(type, handler)` | Register a message handler |
| `setupOffscreenListener()` | Start listening for messages |
| `removeHandler(type)` | Remove a message handler |
| `clearHandlers()` | Remove all handlers |

### Offscreen Reasons

```typescript
"TESTING" | "AUDIO_PLAYBACK" | "BLOBS" | "CLIPBOARD" | "DOM_PARSER"
| "DOM_SCRAPING" | "GEOLOCATION" | "LOCAL_STORAGE" | "MATCH_MEDIA" | "WORKERS"
```

## License

MIT

---

Built by [theluckystrike](https://github.com/theluckystrike) — [zovo.one](https://zovo.one)

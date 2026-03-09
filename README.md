# webext-offscreen

[![npm version](https://img.shields.io/npm/v/webext-offscreen.svg)](https://www.npmjs.com/package/webext-offscreen)
[![CI](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml/badge.svg)](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml)
[![TypeScript](https://img.shields.io/badge/TypeScript-ready-blue.svg)](https://www.typescriptlang.org/)
[![MIT License](https://img.shields.io/npm/l/webext-offscreen.svg)](https://opensource.org/licenses/MIT)

Typed offscreen document creation and messaging for Chrome extensions.

## Why Offscreen Documents?

Chrome's Manifest V3 (MV3) replaced persistent background pages with service workers. While more memory-efficient, service workers **can't access the DOM** — a significant limitation for extensions that need to:

- Parse HTML/XML using `DOMParser`
- Play audio with the Web Audio API
- Manipulate images on `<canvas>` elements
- Access clipboard from background scripts
- Use geolocation features directly

**Offscreen documents** solve this. They're hidden browser contexts providing full DOM access for specific tasks. They have a lifecycle (created on-demand, closed when idle) and communicate with your service worker via message passing.

## Features

- **🏗️ Easy Creation** — One-call offscreen document creation with reason types
- **💬 Typed Messaging** — Send and receive messages with full TypeScript support
- **🔄 Auto-Lifecycle** — Create when needed, close when done
- **📋 Reason Types** — Pre-defined valid reasons (`DOM_PARSER`, `AUDIO_PLAYBACK`, `CLIPBOARD`, etc.)
- **👥 Singleton Management** — Ensure only one document exists
- **🧹 Helper Pattern** — Reusable helper for clean lifecycle management

## Install

```bash
npm install webext-offscreen
```

## Quick Start

### Service Worker (Background)

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

### Offscreen Document

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

```typescript
// Service worker
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Extract metadata from HTML",
});

await offscreen.ensure();
const metadata = await offscreen.send("extract-metadata", { html: fetchedHtml });

// Offscreen document
onOffscreenMessage("extract-metadata", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return {
    title: doc.querySelector("title")?.textContent,
    description: doc.querySelector('meta[name="description"]')?.content,
  };
});
```

### Audio Playback

```typescript
const audioOffscreen = createOffscreenHelper({
  url: "audio.html",
  reasons: ["AUDIO_PLAYBACK"],
  justification: "Play notification sounds",
});

await audioOffscreen.ensure();
await audioOffscreen.send("play", { url: "/sounds/notify.mp3" });
```

### Canvas/Image Manipulation

```typescript
const canvasOffscreen = createOffscreenHelper({
  url: "canvas.html",
  reasons: ["BLOBS"],
  justification: "Resize images before upload",
});

await canvasOffscreen.ensure();
const resized = await canvasOffscreen.send("resize", {
  imageData: originalBlob,
  width: 800,
  height: 600,
});
```

### Clipboard Access

```typescript
const clipboardOffscreen = createOffscreenHelper({
  url: "clipboard.html",
  reasons: ["CLIPBOARD"],
  justification: "Copy formatted HTML to clipboard",
});

await clipboardOffscreen.ensure();
await clipboardOffscreen.send("copy", {
  html: "<h1>Hello</h1>",
  text: "Hello",
});
```

## API Reference

### Service Worker Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `ensureOffscreen(config)` | Create offscreen document if needed | `Promise<void>` |
| `hasOffscreen()` | Check if document is active | `Promise<boolean>` |
| `closeOffscreen()` | Close active document | `Promise<void>` |
| `sendToOffscreen(type, data)` | Send message to offscreen | `Promise<TOut>` |
| `createOffscreenHelper(config)` | Create reusable helper | `OffscreenHelper` |

### Offscreen Document Functions

| Function | Description |
|----------|-------------|
| `onOffscreenMessage(type, handler)` | Register a message handler |
| `setupOffscreenListener()` | Start listening for messages |
| `removeHandler(type)` | Remove a handler |
| `clearHandlers()` | Remove all handlers |

### OffscreenReason Types

```typescript
"TESTING" | "AUDIO_PLAYBACK" | "BLOBS" | "CLIPBOARD" | "DOM_PARSER"
| "DOM_SCRAPING" | "GEOLOCATION" | "LOCAL_STORAGE" | "MATCH_MEDIA" | "WORKERS"
```

## Permissions

**No special permission required** — Offscreen documents are a core Chrome API. However, you must specify a valid `reason` when creating documents, with a `justification` string explaining why. Chrome reviews may ask about your justifications.

## Part of @zovo/webext

`webext-offscreen` is part of the **@zovo/webext** ecosystem — typed utilities for Chrome extensions:

- [webext-storage](https://github.com/theluckystrike/webext-storage) — Typed storage API
- [webext-messaging](https://github.com/theluckystrike/webext-messaging) — Type-safe messaging

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

---

Built by [theluckystrike](https://github.com/theluckystrike) | [zovo.one](https://zovo.one)

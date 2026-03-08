[![CI](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml/badge.svg)](https://github.com/theluckystrike/webext-offscreen/actions)
[![npm](https://img.shields.io/npm/v/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)

# webext-offscreen

Typed offscreen document creation and messaging for Chrome MV3 extensions — DOM parsing, audio, canvas, and more. Part of [@zovo/webext](https://github.com/theluckystrike/webext).

## Why Offscreen Documents?

Chrome Manifest V3 removed DOM access from service workers. Service workers in extensions can no longer:

- Parse HTML/XML documents
- Play audio or video
- Use Canvas API for image manipulation
- Access the clipboard directly
- Use Web Workers for heavy computation
- Access geolocation
- Use localStorage or sessionStorage

**Offscreen documents** are the solution. They're hidden browser contexts that live alongside your service worker and provide full DOM capabilities. Use them as a bridge to perform DOM-heavy operations from your background script.

## Features

- ✅ **Type-safe API** — Full TypeScript support with typed messages
- ✅ **Create offscreen documents** — Simple configuration with justification reasons
- ✅ **Bi-directional messaging** — Send messages and receive responses (including async)
- ✅ **Auto-close support** — Clean up when done
- ✅ **All MV3 reasons supported** — AUDIO_PLAYBACK, CLIPBOARD, DOM_PARSER, WORKERS, and more
- ✅ **Singleton helper pattern** — Reusable offscreen helpers for clean code
- ✅ **Lightweight** — No dependencies, tiny bundle size

## Install

```bash
npm install @theluckystrike/webext-offscreen
```

Or with pnpm:

```bash
pnpm add @theluckystrike/webext-offscreen
```

## Quick Start

### 1. Create an offscreen document

First, add `offscreen.html` to your extension:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="offscreen.js"></script>
</head>
<body></body>
</html>
```

### 2. Use in your service worker (background)

```typescript
import { ensureOffscreen, sendToOffscreen } from "webext-offscreen";

// Create the offscreen document
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content from external sources",
});

// Send a message and get a response
const result = await sendToOffscreen("parse", { 
  html: "<div><h1>Hello World</h1></div>" 
});

console.log(result.text); // "Hello World"
```

### 3. Handle messages in the offscreen document

```typescript
import { onOffscreenMessage, setupOffscreenListener } from "webext-offscreen";

// Register handlers
onOffscreenMessage("parse", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return { text: doc.body.textContent };
});

// Async handlers are supported too
onOffscreenMessage("fetch", async (data) => {
  const response = await fetch(data.url);
  const json = await response.json();
  return json;
});

// Start listening
setupOffscreenListener();
```

## Use Case Examples

### DOM Parsing (HTML/XML)

```typescript
// Background script
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content from API responses",
});

await offscreen.ensure();

// Extract data from HTML
const productData = await offscreen.send("extract-product", {
  html: responseText,
});

// Result: { title: "...", price: "...", description: "..." }
await offscreen.close();
```

### Audio Playback

```typescript
// Play audio from background without popup
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["AUDIO_PLAYBACK"],
  justification: "Play notification sounds",
});

await sendToOffscreen("play-audio", {
  src: "/sounds/notification.mp3",
  volume: 0.8,
});
```

### Canvas Image Manipulation

```typescript
// Process images in offscreen document
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["BLOBS"],
  justification: "Resize and optimize images",
});

const processed = await sendToOffscreen("process-image", {
  imageData: imageArrayBuffer,
  width: 800,
  height: 600,
  format: "image/png",
});
```

### Clipboard Access

```typescript
// Read/write clipboard from background
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["CLIPBOARD"],
  justification: "Copy extracted data to clipboard",
});

await sendToOffscreen("copy-to-clipboard", {
  text: "Copied from extension!",
});
```

### Web Workers (Heavy Computation)

```typescript
// Use Web Workers for CPU-intensive tasks
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["WORKERS"],
  justification: "Process large datasets",
});

const result = await sendToOffscreen("process-data", {
  records: largeDataset,
  operation: "aggregate",
});
```

### Helper Pattern (Recommended)

For cleaner code, use the helper pattern:

```typescript
import { createOffscreenHelper } from "webext-offscreen";

const parser = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content",
});

// Use throughout your extension
async function parseHTML(html: string) {
  await parser.ensure();
  return parser.send("parse", { html });
}

async function closeParser() {
  await parser.close();
}
```

## API Reference

### Service Worker Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `ensureOffscreen(config)` | Create offscreen document if it doesn't exist | `Promise<void>` |
| `hasOffscreen()` | Check if an offscreen document is currently active | `Promise<boolean>` |
| `closeOffscreen()` | Close the active offscreen document | `Promise<void>` |
| `sendToOffscreen(type, data)` | Send a typed message to the offscreen document | `Promise<T>` |
| `createOffscreenHelper(config)` | Create a reusable helper object | `OffscreenHelper` |

### Offscreen Helper Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `ensure()` | Ensure the offscreen document exists | `Promise<void>` |
| `close()` | Close the offscreen document | `Promise<void>` |
| `isActive()` | Check if document is active | `Promise<boolean>` |
| `send(type, data)` | Send a message | `Promise<T>` |

### Offscreen Document Functions

| Function | Description |
|----------|-------------|
| `onOffscreenMessage(type, handler)` | Register a message handler for a specific type |
| `setupOffscreenListener()` | Start listening for incoming messages |
| `removeHandler(type)` | Remove a specific message handler |
| `clearHandlers()` | Remove all registered handlers |

### Offscreen Reasons

These are the valid reasons for creating an offscreen document (as per Chrome's API):

```typescript
"TESTING" | "AUDIO_PLAYBACK" | "BLOBS" | "CLIPBOARD" | "DOM_PARSER"
| "DOM_SCRAPING" | "GEOLOCATION" | "LOCAL_STORAGE" | "MATCH_MEDIA" | "WORKERS"
```

## Configuration

### Type Definitions

```typescript
interface OffscreenConfig {
  url: string;
  reasons: OffscreenReason[];
  justification: string;
}

interface OffscreenMessage<T = unknown> {
  target: "offscreen";
  type: string;
  data: T;
}

interface OffscreenResponse<T = unknown> {
  type: string;
  data: T;
}
```

## Requirements

- Chrome (or Chromium-based browser) with Manifest V3 support
- Node.js 18+ for development

## Related Packages

Part of the **@zovo/webext** ecosystem:

- [webext-storage](https://github.com/theluckystrike/webext-storage) — Typed storage wrapper
- [webext-messenger](https://github.com/theluckystrike/webext-messenger) — Type-safe messaging
- [webext-manifest](https://github.com/theluckystrike/webext-manifest) — Manifest utilities

## License

MIT

---

Built by [theluckystrike](https://github.com/theluckystrike) — [zovo.one](https://zovo.one)

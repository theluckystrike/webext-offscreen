[![CI](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml/badge.svg)](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![npm downloads](https://img.shields.io/npm/dt/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![bundle size](https://img.shields.io/bundlejs/size/@theluckystrike/webext-offscreen)](https://bundlejs.com/?q=@theluckystrike/webext-offscreen)

# webext-offscreen

<p align="center">
  Type-safe offscreen document creation and messaging for Chrome extensions.
</p>

Part of the [chrome-extension-guide](https://github.com/theluckystrike/chrome-extension-guide) ecosystem — a collection of modern, TypeScript-first libraries for building Chrome extensions.

---

## Features

- **🔒 Type-safe** — Full TypeScript support with typed messages and handlers
- **📦 Lightweight** — Zero dependencies, ~1KB gzipped
- **⚡ Simple API** — Intuitive functions for common offscreen document operations
- **🔄 Helper Pattern** — Reusable `OffscreenHelper` for managing document lifecycle
- **📨 Async Messaging** — Promise-based message passing between service worker and offscreen document
- **🧪 Well Tested** — Comprehensive test suite with Vitest

---

## Installation

```bash
npm install @theluckystrike/webext-offscreen
```

Or with pnpm:

```bash
pnpm add @theluckystrike/webext-offscreen
```

Or with yarn:

```bash
yarn add @theluckystrike/webext-offscreen
```

---

## Quick Start

### 1. Service Worker (Background Script)

```typescript
import { ensureOffscreen, sendToOffscreen } from "@theluckystrike/webext-offscreen";

// Ensure offscreen document exists before sending messages
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content for extraction",
});

// Send a message and wait for response
const result = await sendToOffscreen("parse", { 
  html: "<p>Hello, World!</p>" 
});

console.log(result); // { text: "Hello, World!" }
```

### 2. Offscreen Document (`offscreen.html`)

```typescript
import { onOffscreenMessage, setupOffscreenListener } from "@theluckystrike/webext-offscreen";

// Register message handlers
onOffscreenMessage("parse", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return { text: doc.body.textContent };
});

// Async handlers are supported
onOffscreenMessage("fetch-json", async (data) => {
  const response = await fetch(data.url);
  return response.json();
});

// Start listening for messages
setupOffscreenListener();
```

---

## API Reference

### Service Worker Functions

#### `ensureOffscreen(config)`

Creates an offscreen document if one doesn't already exist. Uses a singleton pattern to prevent creating multiple documents.

```typescript
await ensureOffscreen({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Reason shown to user in Chrome's UI",
});
```

**Parameters:**
- `config.url` — Path to the offscreen HTML document
- `config.reasons` — Array of [valid reasons](#offscreen-reasons) for creating the document
- `config.justification` — Human-readable explanation shown in Chrome's UI

---

#### `hasOffscreen()`

Checks whether an offscreen document is currently active.

```typescript
const isActive = await hasOffscreen();
if (isActive) {
  console.log("Offscreen document is running");
}
```

**Returns:** `Promise<boolean>` — `true` if an offscreen document exists

---

#### `closeOffscreen()`

Closes the active offscreen document if one exists.

```typescript
await closeOffscreen();
```

---

#### `sendToOffscreen(type, data)`

Sends a typed message to the offscreen document and waits for a response.

```typescript
const result = await sendToOffscreen<string, number>("calculate", "42");
// Result is typed as number
```

**Parameters:**
- `type` — Message type identifier (used to route to the correct handler)
- `data` — Payload to send to the offscreen document

**Returns:** `Promise<TOut>` — Response from the offscreen document handler

---

#### `createOffscreenHelper(config)`

Creates a reusable helper object that manages the offscreen document lifecycle.

```typescript
const offscreen = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content",
});

// Use the helper
await offscreen.ensure();
const result = await offscreen.send("parse", { html: "<p>Test</p>" });
const isActive = await offscreen.isActive();
await offscreen.close();
```

**Helper Methods:**
| Method | Description |
|--------|-------------|
| `ensure()` | Creates the offscreen document if needed |
| `close()` | Closes the offscreen document |
| `isActive()` | Checks if the document is active |
| `send(type, data)` | Sends a message to the document |

---

### Offscreen Document Functions

#### `onOffscreenMessage(type, handler)`

Registers a handler for a specific message type.

```typescript
onOffscreenMessage("my-action", (data) => {
  // Synchronous handler
  return { processed: true };
});

onOffscreenMessage("async-action", async (data) => {
  // Async handler - return a Promise
  const result = await doAsyncWork(data);
  return result;
});
```

**Parameters:**
- `type` — Message type to handle
- `handler` — Function that processes the message (sync or async)

---

#### `setupOffscreenListener()`

Starts the message listener. Call this after registering all handlers.

```typescript
// Register handlers first
onOffscreenMessage("handler1", (data) => { /* ... */ });
onOffscreenMessage("handler2", (data) => { /* ... */ });

// Then start listening
setupOffscreenListener();
```

---

#### `removeHandler(type)`

Removes a specific message handler.

```typescript
removeHandler("my-action");
```

---

#### `clearHandlers()`

Removes all registered message handlers.

```typescript
clearHandlers();
```

---

### Offscreen Reasons

When creating an offscreen document, you must specify at least one valid reason:

| Reason | Description |
|--------|-------------|
| `TESTING` | Used for automated tests |
| `AUDIO_PLAYBACK` | Audio playback and processing |
| `BLOBS` | Blob and File API operations |
| `CLIPBOARD` | Clipboard read/write operations |
| `DOM_PARSER` | HTML/XML parsing with DOMParser |
| `DOM_SCRAPING` | Web scraping operations |
| `GEOLOCATION` | Geolocation API access |
| `LOCAL_STORAGE` | LocalStorage operations |
| `MATCH_MEDIA` | Media query matching |
| `WORKERS` | Web Worker creation and management |

---

## Examples

### HTML Parsing

```typescript
// Service Worker
import { ensureOffscreen, sendToOffscreen } from "@theluckystrike/webext-offscreen";

async function extractText(html: string) {
  await ensureOffscreen({
    url: "offscreen.html",
    reasons: ["DOM_PARSER"],
    justification: "Parse HTML to extract text content",
  });
  
  return sendToOffscreen("parse", { html });
}

const text = await extractText("<div><p>Hello <strong>World</strong></p></div>");
// Returns: { text: "Hello World" }
```

```typescript
// offscreen.ts
import { onOffscreenMessage, setupOffscreenListener } from "@theluckystrike/webext-offscreen";

onOffscreenMessage("parse", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return { text: doc.body.textContent?.trim() };
});

setupOffscreenListener();
```

### Fetch with CORS Bypass

```typescript
// Service Worker
import { ensureOffscreen, sendToOffscreen } from "@theluckystrike/webext-offscreen";

async function fetchJson(url: string) {
  await ensureOffscreen({
    url: "offscreen.html",
    reasons: ["DOM_SCRAPING"],
    justification: "Fetch data from external API",
  });
  
  return sendToOffscreen("fetch", { url });
}

const data = await fetchJson("https://api.example.com/data");
```

```typescript
// offscreen.ts
import { onOffscreenMessage, setupOffscreenListener } from "@theluckystrike/webext-offscreen";

onOffscreenMessage("fetch", async (data) => {
  const response = await fetch(data.url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
});

setupOffscreenListener();
```

### Clipboard Operations

```typescript
// Service Worker
import { createOffscreenHelper } from "@theluckystrike/webext-offscreen";

const clipboard = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["CLIPBOARD"],
  justification: "Read clipboard content",
});

await clipboard.ensure();
const content = await clipboard.send("read", {});
await clipboard.close();
```

---

## Chrome Extension Guide

`webext-offscreen` is part of the **chrome-extension-guide** ecosystem — a modern, TypeScript-first collection of libraries for building Chrome extensions.

Explore other libraries in the ecosystem:

- **[chrome-extension-guide](https://github.com/theluckystrike/chrome-extension-guide)** — Main repository with guides and examples
- **[webext-storage](https://github.com/theluckystrike/webext-storage)** — Type-safe storage wrapper
- **[webext-messenger](https://github.com/theluckystrike/webext-messenger)** — Type-safe message passing
- **[webext-polyfill](https://github.com/theluckystrike/webext-polyfill)** — Cross-browser API polyfills

---

## Requirements

- Chrome (or Chromium-based browsers) 114+
- TypeScript 5.0+
- Chrome Extensions Manifest V3

---

## License

MIT © [theluckystrike](https://github.com/theluckystrike)

---

<div align="center">

Built by [theluckystrike](https://github.com/theluckystrike) — [zovo.one](https://zovo.one)

</div>

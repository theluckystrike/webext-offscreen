[![CI](https://github.com/theluckystrike/webext-offscreen/actions/workflows/ci.yml/badge.svg)](https://github.com/theluckystrike/webext-offscreen/actions)
[![npm](https://img.shields.io/npm/v/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![Last Commit](https://img.shields.io/github/last-commit/theluckystrike/webext-offscreen)](https://github.com/theluckystrike/webext-offscreen/commits/main)
[![Stars](https://img.shields.io/github/stars/theluckystrike/webext-offscreen)](https://github.com/theluckystrike/webext-offscreen/stargazers)

# webext-offscreen

Typed offscreen document creation and messaging for Chrome extensions. Simplifies the Chrome Offscreen API with full TypeScript support for creating, managing, and communicating with offscreen documents.

Part of the [chrome-extension-guide](https://github.com/theluckystrike/chrome-extension-guide) ecosystem.

## Why Offscreen Documents?

Chrome offscreen documents allow extensions to perform background tasks that require a DOM environment, such as:
- DOM parsing and scraping
- Audio playback
- Blob operations
- Clipboard access
- Geolocation
- Web Workers

This library provides a type-safe API for managing the offscreen document lifecycle and messaging.

## Install

```bash
npm install @theluckystrike/webext-offscreen
```

## Usage

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

// Register message handlers
onOffscreenMessage("parse", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return { text: doc.body.textContent };
});

// Async handlers are supported
onOffscreenMessage("fetch", async (data) => {
  const response = await fetch(data.url);
  return response.json();
});

// Start listening for messages
setupOffscreenListener();
```

### Complete Example

**Background Script (service-worker.ts):**
```typescript
import { ensureOffscreen, sendToOffscreen, createOffscreenHelper } from "webext-offscreen";

const parser = createOffscreenHelper({
  url: "offscreen.html",
  reasons: ["DOM_PARSER"],
  justification: "Parse HTML content from user requests",
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "parseHTML") {
    // Automatically ensures offscreen document exists
    parser.send("parse", { html: message.html })
      .then(result => sendResponse(result))
      .catch(err => sendResponse({ error: err.message }));
    return true; // Keep channel open for async response
  }
});
```

**Offscreen Document (offscreen.ts):**
```typescript
import { onOffscreenMessage, setupOffscreenListener } from "webext-offscreen";

// Handle HTML parsing requests
onOffscreenMessage("parse", (data) => {
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.html, "text/html");
  return {
    title: doc.querySelector("title")?.textContent || "",
    text: doc.body.textContent?.trim() || "",
  };
});

// Handle fetch requests
onOffscreenMessage("fetch", async (data) => {
  const response = await fetch(data.url, data.options);
  return {
    status: response.status,
    data: await response.json(),
  };
});

setupOffscreenListener();
```

## API Reference

### Service Worker Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `ensureOffscreen(config)` | Creates offscreen document if it doesn't exist | `Promise<void>` |
| `hasOffscreen()` | Checks if offscreen document is currently active | `Promise<boolean>` |
| `closeOffscreen()` | Closes the offscreen document | `Promise<void>` |
| `sendToOffscreen(type, data)` | Sends a typed message to the offscreen document | `Promise<TOut>` |
| `createOffscreenHelper(config)` | Creates a reusable helper object for lifecycle management | `OffscreenHelper` |

### Offscreen Document Functions

| Function | Description |
|----------|-------------|
| `onOffscreenMessage(type, handler)` | Registers a message handler for a specific message type |
| `setupOffscreenListener()` | Initializes the message listener |
| `removeHandler(type)` | Removes a specific message handler |
| `clearHandlers()` | Removes all registered handlers |

### Types

```typescript
// Valid reasons for creating an offscreen document
type OffscreenReason =
  | "TESTING"
  | "AUDIO_PLAYBACK"
  | "BLOBS"
  | "CLIPBOARD"
  | "DOM_PARSER"
  | "DOM_SCRAPING"
  | "GEOLOCATION"
  | "LOCAL_STORAGE"
  | "MATCH_MEDIA"
  | "WORKERS";

// Configuration for creating an offscreen document
interface OffscreenConfig {
  url: string;
  reasons: OffscreenReason[];
  justification: string;
}

// Message structure for communication
interface OffscreenMessage<T = unknown> {
  target: "offscreen";
  type: string;
  data: T;
}

// Response from offscreen document
interface OffscreenResponse<T = unknown> {
  type: string;
  data: T;
}
```

## Project Structure

```
webext-offscreen/
├── src/
│   ├── index.ts        # Main library code
│   └── index.test.ts   # Unit tests
├── package.json        # NPM package configuration
├── tsconfig.json       # TypeScript configuration
├── LICENSE             # MIT license
└── README.md           # This file
```

## License

MIT

---

Built at [zovo.one](https://zovo.one) by [theluckystrike](https://github.com/theluckystrike)

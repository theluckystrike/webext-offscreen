[![npm](https://img.shields.io/npm/v/webext-offscreen)](https://www.npmjs.com/package/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)

# webext-offscreen

Typed offscreen document creation and messaging for Chrome extensions.

Part of the [chrome-extension-guide](https://github.com/niceByte/chrome-extension-guide) ecosystem.

## Install

```bash
npm install webext-offscreen
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

// Option 2: Helper pattern
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

## API

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

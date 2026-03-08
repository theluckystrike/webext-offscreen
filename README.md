<div align="center">

# @theluckystrike/webext-offscreen

Typed offscreen document creation and messaging for Chrome extensions. Manage MV3 offscreen documents with a clean API.

[![npm version](https://img.shields.io/npm/v/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![npm downloads](https://img.shields.io/npm/dm/@theluckystrike/webext-offscreen)](https://www.npmjs.com/package/@theluckystrike/webext-offscreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
![npm bundle size](https://img.shields.io/bundlephobia/minzip/@theluckystrike/webext-offscreen)

[Installation](#installation) · [Quick Start](#quick-start) · [API](#api) · [License](#license)

</div>

---

## Features

- **Document lifecycle** -- create and close offscreen documents
- **Reason types** -- typed reasons for offscreen document creation
- **Messaging** -- send and receive messages to/from offscreen documents
- **Singleton guard** -- prevents creating duplicate offscreen documents
- **Typed** -- full TypeScript support
- **Promise-based** -- async/await for all operations

## Installation

```bash
npm install @theluckystrike/webext-offscreen
```

<details>
<summary>Other package managers</summary>

```bash
pnpm add @theluckystrike/webext-offscreen
# or
yarn add @theluckystrike/webext-offscreen
```

</details>

## Quick Start

```typescript
import { Offscreen } from "@theluckystrike/webext-offscreen";

await Offscreen.create({
  url: "offscreen.html",
  reasons: ["CLIPBOARD"],
  justification: "Clipboard access requires an offscreen document in MV3",
});

await Offscreen.close();
```

## API

| Method | Description |
|--------|-------------|
| `create(options)` | Create an offscreen document |
| `close()` | Close the offscreen document |
| `hasDocument()` | Check if an offscreen document exists |
| `sendMessage(msg)` | Send a message to the offscreen document |

## Permissions

```json
{ "permissions": ["offscreen"] }
```

## Part of @zovo/webext

This package is part of the [@zovo/webext](https://github.com/theluckystrike) family -- typed, modular utilities for Chrome extension development:

| Package | Description |
|---------|-------------|
| [webext-storage](https://github.com/theluckystrike/webext-storage) | Typed storage with schema validation |
| [webext-messaging](https://github.com/theluckystrike/webext-messaging) | Type-safe message passing |
| [webext-tabs](https://github.com/theluckystrike/webext-tabs) | Tab query helpers |
| [webext-cookies](https://github.com/theluckystrike/webext-cookies) | Promise-based cookies API |
| [webext-i18n](https://github.com/theluckystrike/webext-i18n) | Internationalization toolkit |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License -- see [LICENSE](LICENSE) for details.

---

<div align="center">

Built by [theluckystrike](https://github.com/theluckystrike) · [zovo.one](https://zovo.one)

</div>

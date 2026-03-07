import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  ensureOffscreen, hasOffscreen, closeOffscreen, sendToOffscreen,
  onOffscreenMessage, setupOffscreenListener, createOffscreenHelper,
  removeHandler, clearHandlers,
} from "./index";

const globalAny = globalThis as any;

beforeEach(() => {
  vi.clearAllMocks();
  clearHandlers();
  globalAny.chrome = {
    offscreen: {
      createDocument: vi.fn().mockResolvedValue(undefined),
      closeDocument: vi.fn().mockResolvedValue(undefined),
    },
    runtime: {
      getContexts: vi.fn().mockResolvedValue([]),
      sendMessage: vi.fn().mockResolvedValue({ result: "ok" }),
      onMessage: { addListener: vi.fn() },
    },
  };
});

describe("webext-offscreen", () => {
  const config = {
    url: "offscreen.html",
    reasons: ["DOM_PARSER" as const],
    justification: "Parse HTML",
  };

  it("creates an offscreen document", async () => {
    await ensureOffscreen(config);
    expect(globalAny.chrome.offscreen.createDocument).toHaveBeenCalledWith({
      url: "offscreen.html",
      reasons: ["DOM_PARSER"],
      justification: "Parse HTML",
    });
  });

  it("skips creation if document already exists", async () => {
    globalAny.chrome.runtime.getContexts.mockResolvedValue([{ contextType: "OFFSCREEN_DOCUMENT" }]);
    await ensureOffscreen(config);
    expect(globalAny.chrome.offscreen.createDocument).not.toHaveBeenCalled();
  });

  it("checks if offscreen document exists", async () => {
    expect(await hasOffscreen()).toBe(false);
    globalAny.chrome.runtime.getContexts.mockResolvedValue([{ contextType: "OFFSCREEN_DOCUMENT" }]);
    expect(await hasOffscreen()).toBe(true);
  });

  it("closes offscreen document", async () => {
    globalAny.chrome.runtime.getContexts.mockResolvedValue([{ contextType: "OFFSCREEN_DOCUMENT" }]);
    await closeOffscreen();
    expect(globalAny.chrome.offscreen.closeDocument).toHaveBeenCalled();
  });

  it("skips close if no offscreen document", async () => {
    await closeOffscreen();
    expect(globalAny.chrome.offscreen.closeDocument).not.toHaveBeenCalled();
  });

  it("sends message to offscreen document", async () => {
    await sendToOffscreen("parse", { html: "<p>hi</p>" });
    expect(globalAny.chrome.runtime.sendMessage).toHaveBeenCalledWith({
      target: "offscreen",
      type: "parse",
      data: { html: "<p>hi</p>" },
    });
  });

  it("registers a message handler", () => {
    const handler = vi.fn();
    onOffscreenMessage("parse", handler);
    expect(removeHandler("parse")).toBe(true);
  });

  it("sets up offscreen listener", () => {
    setupOffscreenListener();
    expect(globalAny.chrome.runtime.onMessage.addListener).toHaveBeenCalled();
  });

  it("dispatches messages to registered handlers", () => {
    const handler = vi.fn().mockReturnValue({ parsed: true });
    onOffscreenMessage("parse", handler);
    setupOffscreenListener();

    const listener = globalAny.chrome.runtime.onMessage.addListener.mock.calls[0][0];
    const sendResponse = vi.fn();
    listener({ target: "offscreen", type: "parse", data: { html: "<p>" } }, {}, sendResponse);

    expect(handler).toHaveBeenCalledWith({ html: "<p>" });
    expect(sendResponse).toHaveBeenCalledWith({ parsed: true });
  });

  it("handles async message handlers", async () => {
    const handler = vi.fn().mockResolvedValue({ parsed: true });
    onOffscreenMessage("parse", handler);
    setupOffscreenListener();

    const listener = globalAny.chrome.runtime.onMessage.addListener.mock.calls[0][0];
    const sendResponse = vi.fn();
    const returnValue = listener({ target: "offscreen", type: "parse", data: {} }, {}, sendResponse);

    expect(returnValue).toBe(true);
    await vi.waitFor(() => expect(sendResponse).toHaveBeenCalledWith({ parsed: true }));
  });

  it("ignores non-offscreen messages", () => {
    setupOffscreenListener();
    const listener = globalAny.chrome.runtime.onMessage.addListener.mock.calls[0][0];
    const sendResponse = vi.fn();
    const result = listener({ target: "popup", type: "x" }, {}, sendResponse);
    expect(result).toBe(false);
    expect(sendResponse).not.toHaveBeenCalled();
  });

  it("creates an offscreen helper", async () => {
    const helper = createOffscreenHelper(config);
    await helper.ensure();
    expect(globalAny.chrome.offscreen.createDocument).toHaveBeenCalled();
    expect(await helper.isActive()).toBe(false);
  });

  it("removes a handler", () => {
    onOffscreenMessage("test", vi.fn());
    expect(removeHandler("test")).toBe(true);
    expect(removeHandler("test")).toBe(false);
  });

  it("clears all handlers", () => {
    onOffscreenMessage("a", vi.fn());
    onOffscreenMessage("b", vi.fn());
    clearHandlers();
    expect(removeHandler("a")).toBe(false);
    expect(removeHandler("b")).toBe(false);
  });
});

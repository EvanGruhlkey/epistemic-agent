import { useCallback, useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { getCurrentWindow } from "@tauri-apps/api/window";
import { SpeechBubble } from "./SpeechBubble";
import "./App.css";

const DUCK_DRAG_THRESHOLD = 8;

const BUBBLE_HINT =
  "Ask a concept (e.g. “What is debugging?”) or, if you’re stuck on a bug, one line: what you expected vs what happened.";

export default function App() {
  const [bubbleOpen, setBubbleOpen] = useState(false);
  const [draft, setDraft] = useState("");
  const [reply, setReply] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const duckDragRef = useRef<{ x: number; y: number; armed: boolean } | null>(
    null,
  );

  useEffect(() => {
    if (!bubbleOpen) {
      setDraft("");
      setReply(null);
      setError(null);
      setBusy(false);
    }
  }, [bubbleOpen]);

  const beginWindowDrag = useCallback(() => {
    void getCurrentWindow().startDragging();
  }, []);

  const onAsk = useCallback(async () => {
    const text = draft.trim();
    if (!text || busy) return;
    setBusy(true);
    setError(null);
    setReply(null);
    try {
      const out = await invoke<string>("duck_ask", { message: text });
      setReply(out);
    } catch (e) {
      let msg: string;
      if (typeof e === "string") msg = e;
      else if (e && typeof e === "object" && "message" in e)
        msg = String((e as { message: unknown }).message);
      else msg = String(e);
      setError(msg);
    } finally {
      setBusy(false);
    }
  }, [busy, draft]);

  const onRootPointerDown = useCallback(
    (e: React.PointerEvent) => {
      if (e.button !== 0) return;
      if ((e.target as HTMLElement).closest(".no-drag")) return;
      beginWindowDrag();
    },
    [beginWindowDrag],
  );

  const onDuckPointerDown = useCallback((e: React.PointerEvent) => {
    if (e.button !== 0) return;
    duckDragRef.current = {
      x: e.clientX,
      y: e.clientY,
      armed: true,
    };
    (e.currentTarget as HTMLButtonElement).setPointerCapture(e.pointerId);
  }, []);

  const onDuckPointerMove = useCallback(
    (e: React.PointerEvent) => {
      const s = duckDragRef.current;
      if (!s?.armed) return;
      const dx = e.clientX - s.x;
      const dy = e.clientY - s.y;
      if (dx * dx + dy * dy < DUCK_DRAG_THRESHOLD * DUCK_DRAG_THRESHOLD) return;
      s.armed = false;
      duckDragRef.current = null;
      try {
        (e.currentTarget as HTMLButtonElement).releasePointerCapture(
          e.pointerId,
        );
      } catch {
        /* ignore */
      }
      beginWindowDrag();
    },
    [beginWindowDrag],
  );

  const onDuckPointerUp = useCallback((e: React.PointerEvent) => {
    const wasTap = duckDragRef.current?.armed === true;
    duckDragRef.current = null;
    try {
      (e.currentTarget as HTMLButtonElement).releasePointerCapture(
        e.pointerId,
      );
    } catch {
      /* ignore */
    }
    if (wasTap) setBubbleOpen((open) => !open);
  }, []);

  const onDuckPointerCancel = useCallback((e: React.PointerEvent) => {
    duckDragRef.current = null;
    try {
      (e.currentTarget as HTMLButtonElement).releasePointerCapture(
        e.pointerId,
      );
    } catch {
      /* ignore */
    }
  }, []);

  return (
    <div className="root" onPointerDown={onRootPointerDown}>
      <div className="stage">
        <div className="stage-bubble-slot">
          {bubbleOpen && (
            <SpeechBubble
              message={BUBBLE_HINT}
              inputValue={draft}
              onInputChange={setDraft}
              onAsk={onAsk}
              busy={busy}
              reply={reply}
              error={error}
            />
          )}
        </div>
        <button
          type="button"
          className="duck-hit no-drag"
          onPointerDown={onDuckPointerDown}
          onPointerMove={onDuckPointerMove}
          onPointerUp={onDuckPointerUp}
          onPointerCancel={onDuckPointerCancel}
          aria-expanded={bubbleOpen}
          aria-label={
            bubbleOpen
              ? "Rubber duck: tap to hide panel, or drag to move window"
              : "Rubber duck: tap for panel, or drag to move window"
          }
        >
          <img className="duck-img" src="/duck.svg" alt="Rubber duck" />
        </button>
      </div>
    </div>
  );
}

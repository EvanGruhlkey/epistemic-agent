import { useCallback, useRef, useState } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import { SpeechBubble } from "./SpeechBubble";
import "./App.css";

const DUCK_DRAG_THRESHOLD = 8;

const BUBBLE_HINT =
  "What's going wrong? In one line: what did you expect, and what happened instead?";

export default function App() {
  const [bubbleOpen, setBubbleOpen] = useState(false);
  const duckDragRef = useRef<{ x: number; y: number; armed: boolean } | null>(
    null,
  );

  const beginWindowDrag = useCallback(() => {
    void getCurrentWindow().startDragging();
  }, []);

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
          {bubbleOpen && <SpeechBubble message={BUBBLE_HINT} />}
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
              ? "Rubber duck: tap to hide hint, or drag to move window"
              : "Rubber duck: tap for a hint, or drag to move window"
          }
        >
          <img className="duck-img" src="/duck.svg" alt="Rubber duck" />
        </button>
      </div>
    </div>
  );
}

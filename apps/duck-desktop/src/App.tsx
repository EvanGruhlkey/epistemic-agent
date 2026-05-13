import { useCallback, useRef } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import "./App.css";

/** Pixels moved before we treat duck interaction as a window drag (not a release-only tap). */
const DUCK_DRAG_THRESHOLD = 8;

export default function App() {
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

  const clearDuckPointer = useCallback((e: React.PointerEvent) => {
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
        <button
          type="button"
          className="duck-hit no-drag"
          onPointerDown={onDuckPointerDown}
          onPointerMove={onDuckPointerMove}
          onPointerUp={clearDuckPointer}
          onPointerCancel={clearDuckPointer}
          aria-label="Rubber duck — drag to move the window"
        >
          <img className="duck-img" src="/duck.svg" alt="Rubber duck" />
        </button>
      </div>
    </div>
  );
}

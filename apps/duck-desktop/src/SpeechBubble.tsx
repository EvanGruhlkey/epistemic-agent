interface SpeechBubbleProps {
  message: string;
}

/** Soft card + tail toward the duck . */
export function SpeechBubble({ message }: SpeechBubbleProps) {
  return (
    <div className="speech-bubble no-drag" role="status" aria-live="polite">
      <div className="speech-bubble-inner">
        <p className="speech-bubble-text">{message}</p>
      </div>
    </div>
  );
}

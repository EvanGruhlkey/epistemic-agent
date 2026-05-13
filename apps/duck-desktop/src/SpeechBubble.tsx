import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface SpeechBubbleProps {
  message: string;
  inputValue: string;
  onInputChange: (value: string) => void;
  inputPlaceholder?: string;
  onAsk: () => void;
  busy: boolean;
  reply: string | null;
  error: string | null;
}

/** Soft card + tail; hint, input, Ask, and reply area. */
export function SpeechBubble({
  message,
  inputValue,
  onInputChange,
  inputPlaceholder = "Describe the bug, your theory, or paste an error…",
  onAsk,
  busy,
  reply,
  error,
}: SpeechBubbleProps) {
  return (
    <div className="speech-bubble no-drag" role="region" aria-label="Rubber duck chat">
      <div className="speech-bubble-inner">
        <p className="speech-bubble-text">{message}</p>
        <label className="speech-bubble-label" htmlFor="duck-input">
          Your input
        </label>
        <textarea
          id="duck-input"
          className="speech-bubble-input"
          rows={3}
          value={inputValue}
          placeholder={inputPlaceholder}
          onChange={(e) => onInputChange(e.target.value)}
          disabled={busy}
          spellCheck
        />
        <div className="speech-bubble-actions">
          <button
            type="button"
            className="speech-bubble-ask"
            disabled={busy || !inputValue.trim()}
            onClick={onAsk}
          >
            {busy ? "Thinking…" : "Ask the duck"}
          </button>
        </div>
        {error && (
          <pre className="speech-bubble-error" role="alert">
            {error}
          </pre>
        )}
        {reply && (
          <div className="speech-bubble-reply-wrap">
            <p className="speech-bubble-reply-label">Reply</p>
            <div className="speech-bubble-reply markdown-reply">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  a: ({ href, children, ...rest }) => (
                    <a
                      {...rest}
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {children}
                    </a>
                  ),
                }}
              >
                {reply}
              </ReactMarkdown>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

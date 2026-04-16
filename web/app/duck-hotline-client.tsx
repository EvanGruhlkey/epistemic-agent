"use client";

import { useState } from "react";

export function DuckHotlineClient() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setReply(null);
    setLoading(true);
    try {
      const res = await fetch("/api/duck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = (await res.json()) as { reply?: string; error?: string; offline?: boolean };
      if (!res.ok) {
        setError(data.error ?? `Request failed (${res.status})`);
        return;
      }
      setReply(data.reply ?? "");
    } catch {
      setError("Network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full max-w-2xl space-y-6">
      <form onSubmit={onSubmit} className="space-y-3 text-left">
        <label htmlFor="msg" className="block text-sm font-medium text-foreground">
          What are you stuck on?
        </label>
        <textarea
          id="msg"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
          className="w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 shadow-sm focus:border-neutral-500 focus:outline-none focus:ring-1 focus:ring-neutral-500 dark:border-neutral-700 dark:bg-neutral-950 dark:text-neutral-100"
          placeholder="Describe the bug, confusion, or design tension — no code paste required."
          required
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-lg bg-neutral-900 px-4 py-2 text-sm font-medium text-white hover:bg-neutral-800 disabled:opacity-50 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-white"
        >
          {loading ? "Thinking…" : "Ask the duck"}
        </button>
      </form>

      {error && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-950 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-100">
          <p className="font-medium">Heads up</p>
          <p className="mt-1 whitespace-pre-wrap">{error}</p>
          <p className="mt-2 text-xs text-amber-800 dark:text-amber-200">
            In Cursor or Claude Code, use <code className="rounded bg-amber-100 px-1 dark:bg-amber-900">/duck-hotline</code>{" "}
            — no API key needed there.
          </p>
        </div>
      )}

      {reply && (
        <div className="rounded-lg border border-neutral-200 bg-white px-4 py-3 text-left text-sm text-neutral-800 shadow-sm dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-200">
          <p className="font-medium text-foreground">Duck says</p>
          <div className="mt-2 whitespace-pre-wrap">{reply}</div>
        </div>
      )}
    </div>
  );
}

import { DuckHotlineClient } from "./duck-hotline-client";

export default function Home() {
  return (
    <div className="flex min-h-full flex-1 flex-col items-center justify-center px-6 py-16">
      <main className="flex w-full max-w-2xl flex-col items-center space-y-8 text-center">
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold tracking-tight text-foreground">
            Duck Hotline
          </h1>
          <p className="text-sm text-neutral-600 dark:text-neutral-400">
            Questions and pointers only — you keep the keyboard. Pair programming, not
            auto-coding.
          </p>
        </div>
        <DuckHotlineClient />
        <p className="max-w-lg text-xs text-neutral-500 dark:text-neutral-500">
          Prefer your IDE? Open <code className="rounded bg-neutral-100 px-1 dark:bg-neutral-900">AGENTS.md</code> and run{" "}
          <code className="rounded bg-neutral-100 px-1 dark:bg-neutral-900">/duck-hotline</code> in Claude Code, or follow
          Cursor rules in <code className="rounded bg-neutral-100 px-1 dark:bg-neutral-900">.cursor/rules/</code>.
        </p>
      </main>
    </div>
  );
}

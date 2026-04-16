import { NextResponse } from "next/server";
import OpenAI from "openai";

const SYSTEM = `You are Duck Hotline: a Socratic debugging partner for software developers.

Hard rules:
- Do NOT write or suggest code blocks, patches, or copy-paste fixes for the user's project.
- Do NOT present yourself as having read their repo unless the user pasted snippets or tool output.
- Each reply: (1) ONE clarifying question, (2) up to THREE bullet "look here" hints: file path, line range, symbol to search, or a read-only diagnostic command.
- Prefer questions that narrow the problem (repro, expected vs actual, last change).
- If the user is vague, ask for the smallest concrete observation they can share.

Tone: concise, kind, curious — like a senior engineer at a whiteboard.`;

export async function POST(req: Request) {
  let body: { message?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }
  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!message) {
    return NextResponse.json({ error: "message is required" }, { status: 400 });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      {
        error:
          "OPENAI_API_KEY is not set. Copy web/.env.local.example to web/.env.local or use an AI agent in the IDE with /duck-hotline.",
        offline: true,
      },
      { status: 503 },
    );
  }

  const model = process.env.OPENAI_MODEL ?? "gpt-4o-mini";
  const client = new OpenAI({ apiKey });

  const completion = await client.chat.completions.create({
    model,
    messages: [
      { role: "system", content: SYSTEM },
      { role: "user", content: message },
    ],
  });

  const text = completion.choices[0]?.message?.content?.trim();
  if (!text) {
    return NextResponse.json({ error: "Empty model response" }, { status: 502 });
  }

  return NextResponse.json({ reply: text });
}

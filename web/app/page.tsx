
"use client";

import { useState } from "react";

type Message = {
  role: "user" | "assistant";
  text: string;
};

export default function Home() {
  const [term, setTerm] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function explainTerm(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    const input = term.trim();
    if (!input || loading) return;

    setMessages([{ role: "user", text: input }]);
    setTerm("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/explain",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ term: input }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Backend request failed"
        );
      }

      const answer =
  typeof data === "string"
    ? data
    : Array.isArray(data.lines)
      ? data.lines.join("\n")
      : data.raw ??
        data.explanation ??
        data.answer ??
        data.result ??
        JSON.stringify(data, null, 2);

      setMessages([
  { role: "user", text: input },
  { role: "assistant", text: answer },
]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            error instanceof Error
              ? error.message
              : "Could not connect to the backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-12 text-white">
      <div className="mx-auto max-w-2xl">
        <header className="mb-10 text-center">
          <p className="mb-3 text-sm font-semibold tracking-[0.3em] text-cyan-400">
            LEARN AI SIMPLY
          </p>
          <h1 className="text-5xl font-bold">
            Termify<span className="text-cyan-400">😋</span>
          </h1>
          <p className="mt-4 text-slate-400">
            Every technical term, explained in five simple lines.
          </p>
        </header>

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-2 text-xl font-semibold">
            AI Term Explainer
          </h2>
          <p className="mb-6 text-sm text-slate-400">
            Enter a term like RAG, LLM, API, or AI Agent.
          </p>

          <form onSubmit={explainTerm} className="flex gap-2">
            <input
              value={term}
              onChange={(e) => setTerm(e.target.value)}
              placeholder="Enter an AI term..."
              className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-cyan-400"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !term.trim()}
              className="rounded-xl bg-cyan-400 px-4 py-3 font-semibold text-slate-950 disabled:opacity-50"
            >
              {loading ? "..." : "Explain"}
            </button>
          </form>

          <div className="mt-8 space-y-4">
            {messages.map((message, index) => (
              <article
                key={index}
                className="whitespace-pre-wrap break-words rounded-xl border border-slate-800 bg-slate-950 p-5"
              >
                <p className="mb-3 text-xs font-bold uppercase tracking-widest text-cyan-400">
                  {message.role === "user"
                    ? "Your Term"
                    : "AI Term Explainer"}
                </p>
                
<div className="space-y-2 text-sm leading-7 text-slate-200">
  {message.text.split("\n").map((line, i) => {
    const match = line.match(
      /^(Term|Simple|Mental Model|Example|Why it matters):\s*(.*)$/
    );

    return (
      <p key={i}>
        {match ? (
          <>
            <span className="font-bold text-cyan-400">
              {match[1]}:
            </span>{" "}
            <span>{match[2]}</span>
          </>
        ) : (
          line
        )}
      </p>
    );
  })}
</div>

              </article>
            ))}

            {loading && (
              <p className="animate-pulse text-sm text-cyan-400">
                Explaining your term...
              </p>
            )}
          </div>
        </section>

        <footer className="mt-6 text-center text-xs text-slate-500">
          Termify · Simple explanations. Clear understanding.
        </footer>
      </div>
    </main>
  );
}

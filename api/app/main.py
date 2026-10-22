# pip install -qU langchain langchain-ollama
import difflib
import json
from pathlib import Path

from langchain.agents import create_agent

# glossary.json ko main.py ke saath same folder me rakho
# api/app/main.py se ek folder upar jao, phir data/glossary.json
GLOSSARY_PATH = Path(__file__).resolve().parent.parent / "data" / "glossary.json"

with open(GLOSSARY_PATH, encoding="utf-8") as f:
    _data = json.load(f)

# dono format chalte hain: {"terms": [...]} ya seedhi list [...]
GLOSSARY = _data["terms"] if isinstance(_data, dict) else _data


def _aliases(term: str) -> list[str]:
    """'RAG (Retrieval-Augmented Generation)' -> ['rag (retrieval-augmented generation)', 'rag', 'retrieval-augmented generation']"""
    full = term.lower()
    names = [full]
    if "(" in full and full.endswith(")"):
        short, long_ = full[:-1].split("(", 1)
        names += [short.strip(), long_.strip()]
    return names


def lookup_term(term: str) -> str:
    """Look up an AI term in the glossary and return its official one-line description.
    Always call this first when the user asks about an AI term (e.g. RAG, LoRA, MCP)."""
    query = term.strip().lower()

    # 1) exact match (full name, short form, or long form)
    for item in GLOSSARY:
        if query in _aliases(item["term"]):
            return json.dumps(item, ensure_ascii=False)

    # 2) close matches (typos / partial names)
    all_names = {alias: item for item in GLOSSARY for alias in _aliases(item["term"])}
    close = difflib.get_close_matches(query, all_names.keys(), n=3, cutoff=0.6)
    if close:
        return json.dumps(
            {
                "found": False,
                "did_you_mean": [all_names[c]["term"] for c in close],
            },
            ensure_ascii=False,
        )

    return json.dumps({"found": False, "message": "Term not in glossary"})


SYSTEM_PROMPT = """You are an AI Term Explainer.

For every AI term the user asks about:
1. Call the lookup_term tool first.
2. If the term is found, use its description as the base of your answer.
3. If it is not found but did_you_mean has suggestions, use the closest one and say so.
4. If it is not in the glossary at all, say "Not in glossary" in line 1 and answer carefully from your own knowledge.

Answer in EXACTLY 5 lines, one short sentence per line, no extra text, no markdown:
Line 1 - Term: the full name of the term.
Line 2 - Simple: a one-line plain explanation (from the glossary description).
Line 3 - Mental Model: a one-line analogy to picture it.
Line 4 - Example: a one-line real-world AI example.
Line 5 - Why it matters: a one-line reason it is useful or important.
"""

agent = create_agent(
    model="ollama:gemma4:31b-cloud",
    tools=[lookup_term],
    system_prompt=SYSTEM_PROMPT,
)


def explain(term: str) -> str:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Explain this AI term: {term}"}]}
    )
    return result["messages"][-1].text


if __name__ == "__main__":
    print("AI Term Explainer (type 'exit' to quit)")
    while True:
        term = input("\nTerm: ").strip()
        if term.lower() in {"exit", "quit", "q"}:
            break
        if term:
            print(explain(term))
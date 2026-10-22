# Termify

Understand AI jargon in 5 lines. Termify is an AI term explainer: type any AI term (like RAG, LoRA, or MCP) and get a short, clear explanation backed by a glossary of 227 terms.

## What you get

For every term, the agent answers in exactly 5 lines:

1. **Term**: the full name
2. **Simple**: a one-line plain explanation
3. **Mental Model**: a one-line analogy
4. **Example**: a one-line real-world example
5. **Why it matters**: why the term is useful or important

Example (RAG):

```
Term: RAG (Retrieval-Augmented Generation)
Simple: A technique where a model retrieves relevant information from external sources before answering.
Mental Model: Like an open-book exam instead of answering from memory.
Example: A support chatbot that searches your company docs before replying.
Why it matters: It makes answers more accurate and up to date.
```

## How it works

- `api/data/glossary.json` holds the glossary (AI term + one-line description).
- The agent in `api/app/main.py` is built with [LangChain](https://www.langchain.com/) and calls a `lookup_term` tool to fetch the glossary description first.
- It then writes the 5-line answer using an Ollama model (`gemma4:31b-cloud`).
- If a term is not in the glossary, the agent says so and answers from its own knowledge. If the spelling is close, it suggests the right term.

## Project structure

```
termify/
├── api/
│   ├── app/
│   │   └── main.py          # LangChain agent + CLI
│   ├── data/
│   │   └── glossary.json    # AI glossary (term + description)
│   ├── src/
│   └── pyproject.toml
├── web/
└── README.md
```

## Getting started

**Requirements**

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/) (cloud models need you to be signed in to Ollama)

**Run it**

```bash
cd api
uv sync
cd app
uv run main.py
```

Type a term when prompted, or `exit` to quit.

```
AI Term Explainer (type 'exit' to quit)

Term: RAG
```

## Glossary format

```json
{
  "terms": [
    {
      "term": "RAG (Retrieval-Augmented Generation)",
      "description": "A technique where a model retrieves relevant information from external sources and uses it to generate a grounded answer."
    }
  ]
}
```

To add a term, append a new object to the `terms` list. Keep each description to one line.

## Roadmap

- Web interface in `web/`
- API endpoint for explaining terms
- More terms and categories

## Contributing

Found a wrong or missing term? Open an issue or a pull request with the term and a one-line description.
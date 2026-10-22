from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.main import GLOSSARY, explain

app = FastAPI(title="Termify API")

# Next.js frontend (localhost:3000) ko backend call karne ki ijazat
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExplainRequest(BaseModel):
    term: str


@app.get("/api/health")
def health():
    return {"status": "ok", "terms": len(GLOSSARY)}


@app.get("/api/terms")
def list_terms():
    """Glossary ki poori list (search / autocomplete ke liye)."""
    return {"count": len(GLOSSARY), "terms": GLOSSARY}


@app.post("/api/explain")
def explain_term(body: ExplainRequest):
    """Agent se term ka 5 lines wala jawab."""
    term = body.term.strip()
    if not term:
        raise HTTPException(status_code=400, detail="term is required")

    try:
        raw = explain(term)
    except Exception as e:
        # Ollama band ho, model na mile, ya sign in na ho to yahan aayega
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    return {"term": term, "lines": lines, "raw": raw}
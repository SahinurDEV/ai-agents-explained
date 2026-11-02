# Step 5 - RAG with Chroma

**Course link:** Module 4 (RAG & vector DBs) · Section 10 of *AI Agents Explained*

## What you build
Chunk `docs/*.md`, embed, store in a local Chroma DB, retrieve top-k chunks via a `search_docs` tool, answer with `[source]` citations.

## Run it
```bash
cd project
python step05_rag/rag.py "How long do I have to ask for a refund?"
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Add your own markdown file to `docs/` and ask about it. Try `EMBED_PROVIDER=openai` and compare retrieval quality.

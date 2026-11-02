# Module 08 Capstone - Reference Architecture: "Study Buddy"

An agent that helps you revise this course from your own notes.

| Layer | Implementation (from `project/`) |
|---|---|
| Model | `common/llm.py` (Ollama `llama3.1` free, or any OpenAI-compatible API) |
| Instructions | System prompt: "Quiz me, cite my notes, never invent facts" |
| Tools | `calculator`, `make_flashcard(front, back)`, `get_time` |
| Memory | step 4 `MemoryStore`: weak topics, preferred quiz length |
| Knowledge | step 5 `KnowledgeBase` over your lecture notes (`docs/`) |
| Connections | step 6 MCP notes server for saving flashcards |
| Safeguards | step 7 `GuardedAgent`: allowlist, budget, approval for deletes, audit |

Flow: user asks "Quiz me on RAG" -> `search_docs("RAG")` -> generate 3 questions with sources -> user answers -> agent grades, saves weak topics to memory -> `add_note` flashcards via MCP.

## Rubric (100)
- Works end-to-end with a real or local model - 25
- Uses >= 2 tools correctly, errors handled - 15
- Memory persists across sessions - 10
- RAG answers cite sources - 15
- MCP tool discovered at runtime - 10
- Guardrails + audit log - 15
- README diagram + 5 offline tests - 10

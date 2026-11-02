# Step 4 - Memory

**Course link:** Module 3 (memory & state) · Section 10 of *AI Agents Explained*

## What you build
Short-term memory = recent chat history (trimmed to `max_history`). Long-term memory = facts in `memory.json`, injected into the system prompt next session.

## Run it
```bash
cd project
python step04_memory/agent.py
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Tell it a fact, quit, restart, and ask about it. Open `memory.json` - memory is just data you can inspect and delete.

# Step 1 - A plain LLM call

**Course link:** Module 1 (LLM foundations) · Section 10 of *AI Agents Explained*

## What you build
Send a system + user message, print the reply. This is a chatbot, not an agent yet.

## Run it
```bash
cd project
python step01_llm_call/main.py "What is an AI agent?"
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Change the system prompt to answer as a pirate. What changes? What does NOT change (it still can't look anything up)?

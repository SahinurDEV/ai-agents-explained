# Step 3 - The agent loop

**Course link:** Module 2 (reason-act loop) · Section 10 of *AI Agents Explained*

## What you build
Repeat: model decides -> runtime executes -> observation goes back, until a final answer or `max_steps`. Tool errors become observations instead of crashes.

## Run it
```bash
cd project
python step03_agent_loop/agent.py "What's the weather in Dhaka and what is 31*9/5+32?"
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Print `agent.trace` after a run. Lower `max_steps` to 1 and see the limit work.

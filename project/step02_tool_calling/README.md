# Step 2 - Tool calling

**Course link:** Module 3 (tools & APIs) · Section 10 of *AI Agents Explained*

## What you build
The model returns a *request* to call `calculator` or `get_weather`. Our code runs the function and sends the result back.

## Run it
```bash
cd project
python step02_tool_calling/main.py "What is 1234 * 56?"
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Add a `get_time(city)` tool: a function + a schema in `common/tools.py`.

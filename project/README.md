# Hands-On Project: Build Your Own AI Agent

Seven small steps, each a working program that adds ONE idea to the previous one.
Matches **Section 10** of the Udemy course *AI Agents Explained*.

| Step | Folder | You add | Course module |
|---|---|---|---|
| 1 | [step01_llm_call](step01_llm_call) | A plain LLM call | 1 |
| 2 | [step02_tool_calling](step02_tool_calling) | Tool calling | 3 |
| 3 | [step03_agent_loop](step03_agent_loop) | The reason-act loop | 2 |
| 4 | [step04_memory](step04_memory) | Short + long-term memory | 3 |
| 5 | [step05_rag](step05_rag) | RAG with Chroma + citations | 4 |
| 6 | [step06_mcp](step06_mcp) | MCP server + client | 4 |
| 7 | [step07_guardrails](step07_guardrails) | Safety and guardrails | 7 |

Shared code: `common/llm.py` (one client for OpenAI-compatible APIs, Ollama, or an offline mock) and `common/tools.py`.

## Setup (5 minutes)
```bash
git clone https://github.com/SahinurDEV/ai-agents-explained.git
cd ai-agents-explained
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # choose mock, Ollama (free) or an API key
```

## Choose a model
- **No key, offline:** `LLM_PROVIDER=mock` - a rule-based fake model so every code path runs. Great for learning the plumbing; not smart.
- **Free, local:** install [Ollama](https://ollama.com), run `ollama pull llama3.1`, set `LLM_PROVIDER=ollama`. Pick a model that supports tool calling (llama3.1, qwen2.5).
- **Hosted API:** any OpenAI-compatible provider: set `LLM_PROVIDER=openai`, `LLM_API_KEY`, `LLM_MODEL` and, if not OpenAI, `LLM_BASE_URL`.

## Run
```bash
cd project
python step01_llm_call/main.py "What is an AI agent?"
python step03_agent_loop/agent.py "What's the weather in Dhaka?"
bash smoke.sh          # runs all 7 steps offline
pytest -q tests        # 9 offline tests
```

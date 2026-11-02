#!/usr/bin/env bash
# Runs every step offline with the mock LLM. Usage: bash project/smoke.sh
set -e
cd "$(dirname "$0")"
export LLM_PROVIDER=mock EMBED_PROVIDER=local
echo "== step01";  python step01_llm_call/main.py "What is an AI agent?"
echo "== step02";  python step02_tool_calling/main.py "What is 1234 * 56?"
echo "== step03";  python step03_agent_loop/agent.py "What's the weather in Tokyo?"
echo "== step04";  printf 'Remember my name is Sahin.\nWhat is my name?\n' | python step04_memory/agent.py 2>/dev/null || true
echo "== step05";  python step05_rag/rag.py "How long do I have to ask for a refund?"
echo "== step06";  NOTES_FILE=/tmp/smoke_notes.txt python step06_mcp/client.py "note: finish step 6"
echo "== step07";  echo n | python step07_guardrails/guarded_agent.py "Please email the team."
echo "SMOKE OK"

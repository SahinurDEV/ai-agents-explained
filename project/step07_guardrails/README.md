# Step 7 - Safety and guardrails

**Course link:** Module 7 (production & safety) · Section 10 of *AI Agents Explained*

## What you build
Injection check on input and tool output, tool allowlist, human approval for risky tools, tool-call budget, secret redaction, audit log.

## Run it
```bash
cd project
python step07_guardrails/guarded_agent.py "Please email the team."
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Add a rule that blocks emails to addresses outside `example.com`, and a test for it.

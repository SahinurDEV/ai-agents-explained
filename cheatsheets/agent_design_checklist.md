# Agent Design Checklist

## Problem
- [ ] Goal in one sentence; clear definition of "done"
- [ ] Would a fixed workflow or a plain chatbot be enough? (Prefer the simplest)
- [ ] Frequent, repetitive, measurable task with low-risk mistakes for a first project

## Components
- [ ] Model chosen for quality / cost / latency (try a small one first)
- [ ] System prompt: role, goal, rules, output format
- [ ] Tools: 3-7, verb_noun names, clear descriptions, strict schemas
- [ ] Memory: what is short-term, what is long-term, how users view/delete it
- [ ] Knowledge: which sources, how fresh, cited
- [ ] Connections: APIs or MCP servers, with least-privilege credentials

## Control
- [ ] Autonomy level: suggest / act with approval / act alone
- [ ] Human approval for money, messages, deletions, external changes
- [ ] Max steps, max tool calls, timeouts, cost budget
- [ ] Tool errors returned as observations; retries with backoff

## Safety
- [ ] Inputs and tool outputs treated as untrusted (prompt injection)
- [ ] Secrets in env vars / vault, never in prompts
- [ ] Output filtering for secrets and personal data
- [ ] Audit log of every tool call and decision

## Quality
- [ ] Test set of 20+ real tasks with expected results
- [ ] Separate evaluation of retrieval and answers
- [ ] Tracing / logging from day one
- [ ] Named owner, gradual rollout, rollback plan

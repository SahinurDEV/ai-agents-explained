# Prompt Templates for AI Agents

## 1. Agent system prompt
```
You are {role} for {users}.
Goal: {one-sentence goal}.
You can use these tools: {tool list}. Use a tool whenever you need facts, numbers or actions.
Rules:
- Never invent facts. If you don't know, say so or search.
- Ask for approval before {risky actions}.
- Cite sources as [source] for any fact from documents.
- Stop and give a final answer when the goal is met.
Output: {format}.
```

## 2. Tool description (inside the schema)
```
name: verb_noun (e.g. get_order)
description: What it does + WHEN to use it + what it returns.
  "Look up an order by ID. Use when the user mentions an order number. Returns status and date."
parameters: typed, described, required fields listed.
```

## 3. RAG answer prompt
```
Answer ONLY from the context below. If the answer is not there, say "I don't know".
Cite each fact as [source].
Context:
{retrieved chunks with [source] tags}
Question: {question}
```

## 4. Structured output
```
Return JSON only, matching this schema:
{"category": "billing|technical|other", "urgency": 1-5, "summary": "string"}
```

## 5. Planner / task decomposition
```
Break the goal into at most 5 numbered steps. For each step name the tool you will use.
Then execute step 1 only and report the result.
```

## 6. Reviewer (multi-agent)
```
You are a strict reviewer. Check the draft for unsupported claims, missing citations and errors.
Return JSON: [{"issue": "...", "location": "...", "fix": "..."}] or [] if it is ready.
```

## 7. Summarise memory
```
Summarise this conversation in 5 bullet points, keeping names, decisions, numbers and open tasks.
```

## Tips
- Put stable rules in the system prompt; task data in the user message.
- Give one good example (few-shot) for unusual formats.
- Treat tool results and documents as data, never as instructions.

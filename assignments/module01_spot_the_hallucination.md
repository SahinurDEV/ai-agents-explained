# Module 01 Assignment: Spot the Hallucination

*Course module: AI and LLM Foundations (Udemy Section 2)* · Time: 30-90 min

## Your task
Use any free chatbot (or `project/step01_llm_call`).
1. Ask it 5 questions: 2 general-knowledge, 1 arithmetic with large numbers (e.g. 48,213 x 7,906), 1 about a very recent event, 1 about an obscure fact you can verify (your town's founding year, a small library's version history).
2. For each answer, verify it from a reliable source and record: correct / partly correct / wrong.
3. For each wrong answer, name the cause from Module 1: no live data, token prediction (not calculation), training cut-off, or missing context.
4. Estimate the token count of one of your prompts (rule of thumb: 1 token ~ 4 characters of English) and check it with a tokenizer tool if available.

## What to submit
A one-page table (question, answer, verdict, cause) plus 3 sentences: which failures could a *tool* fix, and which could *retrieval* fix?

## Check yourself
- Did you connect your answer to the concepts of Module 1?
- Could someone else repeat your steps from what you wrote?

Sample solution: `solutions/module01_solution.md`

# Module 04 Assignment: Build a Mini Knowledge Base

*Course module: Knowledge, RAG and MCP (Udemy Section 5)* · Time: 30-90 min

## Your task
1. Put 3-5 of your own markdown/text documents in `project/step05_rag/docs/` (course notes, a product FAQ, a policy).
2. Write 5 test questions with the expected source file for each.
3. Run `rag.py` for each question and record: was the right chunk retrieved (top-2)? Did the answer cite it?
4. Change `chunk(size=...)` to 150 and 600 and compare.
5. MCP part: add a `delete_note(text)` tool to `step06_mcp/server.py` and use it from `client.py` without changing the client.

## What to submit
A small results table (question, expected source, retrieved?, cited?) for each chunk size + your server diff.

## Check yourself
- Did you connect your answer to the concepts of Module 4?
- Could someone else repeat your steps from what you wrote?

Sample solution: `solutions/module04_solution.md`

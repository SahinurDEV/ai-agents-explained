# Module 05 Sample Solution: Workflow or Agent?

(a) Workflow: extract -> validate -> write; deterministic and testable. An LLM may be one step (extraction), not the controller.
(b) Single agent with tools `search_docs`, `get_order(id)`, and human hand-off; the path varies by question.
(c) Multi-agent can help: Researcher (search, read) -> Writer (draft with citations) -> Reviewer (checks claims, returns issues as JSON `{issue, location, fix}`); stop after 2 review rounds. Compare against a single agent first.
(d) Scheduled workflow / cron job - no agent needed. The cheapest reliable design wins.

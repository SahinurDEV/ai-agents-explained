# Module 07 Sample Solution: Red-Team Your Agent

See `solutions/module07_domain_guardrail.py` and its test. Notes:
- Regex injection checks are a *first layer* only; real protection comes from least privilege, approvals and treating tool output as untrusted data.
- Budgets (max steps / tool calls) stop runaway loops and cost.
- Keep the eval set in version control and run it on every prompt or model change.

"""Step 7: safety and guardrails around the same agent loop.

1. Input check   - flag obvious prompt-injection phrases in user text and tool results.
2. Allowlist     - the agent may only call tools we list.
3. Approval      - risky tools (send_email, delete_file) need a human 'yes'.
4. Limits        - max steps and max tool calls per run.
5. Output filter - redact things that look like secrets before showing the answer.
6. Audit log     - every decision is recorded.
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.tools import TOOLS, SCHEMAS, schema
from step03_agent_loop.agent import Agent

INJECTION = re.compile(r"ignore (all|previous|prior) instructions|reveal (the )?system prompt|you are now", re.I)
SECRET = re.compile(r"(sk-[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{16}|\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b)")


def send_email(to: str, body: str) -> str:
    return f"(demo) email to {to} queued"          # never really sends


def delete_file(path: str) -> str:
    return f"(demo) would delete {path}"           # never really deletes


RISKY = {"send_email", "delete_file"}


class GuardedAgent(Agent):
    def __init__(self, approve=None, allowed=None, max_tool_calls=5, **kw):
        tools = dict(TOOLS, send_email=send_email, delete_file=delete_file)
        schemas = SCHEMAS + [
            schema("send_email", "Send an email.", to=("string", "Recipient"), body=("string", "Text")),
            schema("delete_file", "Delete a file.", path=("string", "File path"))]
        self.allowed = set(allowed or tools)
        super().__init__(tools=tools, schemas=[s for s in schemas if s["function"]["name"] in self.allowed], **kw)
        self.approve = approve or (lambda name, args: input(f"Allow {name}({args})? [y/N] ").strip().lower() == "y")
        self.max_tool_calls, self.calls, self.audit = max_tool_calls, 0, []

    def run_tool(self, name, args):
        self.calls += 1
        if self.calls > self.max_tool_calls:
            decision = "blocked: tool-call budget exceeded"
        elif name not in self.allowed:
            decision = f"blocked: {name} is not on the allowlist"
        elif name in RISKY and not self.approve(name, args):
            decision = f"blocked: human did not approve {name}"
        else:
            result = super().run_tool(name, args)
            if INJECTION.search(result):
                result = "[tool result removed: possible prompt injection]"
            decision = result
        self.audit.append((name, args, decision))
        return decision

    def run(self, goal, messages=None):
        if INJECTION.search(goal):
            self.audit.append(("input", goal, "refused: possible prompt injection"))
            return "Sorry, I can't follow that request."
        return SECRET.sub("[REDACTED]", super().run(goal, messages) or "")


if __name__ == "__main__":
    a = GuardedAgent()
    print(a.run(" ".join(sys.argv[1:]) or "Please email the team the weekly summary."))
    for row in a.audit:
        print("audit:", row)

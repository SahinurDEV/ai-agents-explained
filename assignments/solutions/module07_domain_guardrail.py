"""Module 7 solution: only allow emails to one domain, plus a test. Run: pytest assignments/solutions/module07_domain_guardrail.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "project"))
os.environ.setdefault("LLM_PROVIDER", "mock")
from common.llm import MockLLM
from step07_guardrails.guarded_agent import GuardedAgent

ALLOWED_DOMAIN = "example.com"


class DomainGuardedAgent(GuardedAgent):
    def run_tool(self, name, args):
        if name == "send_email" and not str(args.get("to", "")).endswith("@" + ALLOWED_DOMAIN):
            self.audit.append((name, args, "blocked: outside domain"))
            return f"blocked: emails may only go to @{ALLOWED_DOMAIN}"
        return super().run_tool(name, args)


def test_blocks_outside_domain():
    a = DomainGuardedAgent(llm=MockLLM(), approve=lambda n, a: True, verbose=False)
    assert "blocked" in a.run_tool("send_email", {"to": "evil@attacker.io", "body": "hi"})
    assert "queued" in a.run_tool("send_email", {"to": "team@example.com", "body": "hi"})

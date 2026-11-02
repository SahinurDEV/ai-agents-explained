"""Step 3: the agent loop. Reason -> act -> observe, repeated until done or a step limit."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.llm import get_llm
from common.tools import TOOLS, SCHEMAS

SYSTEM = ("You are a helpful agent. Think step by step. Call tools when needed, "
          "one or more times, then give a short final answer.")


class Agent:
    def __init__(self, llm=None, tools=TOOLS, schemas=SCHEMAS, max_steps=6, verbose=True):
        self.llm, self.tools, self.schemas = llm or get_llm(), tools, schemas
        self.max_steps, self.verbose = max_steps, verbose
        self.trace = []                                   # what happened, for debugging

    def run_tool(self, name, args):
        if name not in self.tools:
            return f"error: unknown tool {name}"
        try:
            return str(self.tools[name](**args))
        except Exception as e:                            # tool failures become observations
            return f"error: {e}"

    def run(self, goal, messages=None):
        messages = messages or [{"role": "system", "content": SYSTEM}]
        messages.append({"role": "user", "content": goal})
        for step in range(1, self.max_steps + 1):
            reply = self.llm.chat(messages, tools=self.schemas)
            messages.append(reply.as_message())
            if not reply.tool_calls:                      # no more actions -> final answer
                self.trace.append(("answer", reply.content))
                return reply.content
            for tc in reply.tool_calls:
                obs = self.run_tool(tc.name, tc.arguments)
                self.trace.append((tc.name, tc.arguments, obs))
                if self.verbose:
                    print(f"[step {step}] {tc.name}({json.dumps(tc.arguments)}) -> {obs}")
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        return "Stopped: step limit reached."


if __name__ == "__main__":
    print(Agent().run(" ".join(sys.argv[1:]) or "What's the weather in Dhaka?"))

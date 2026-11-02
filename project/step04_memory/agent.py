"""Step 4: memory. Short-term = trimmed chat history. Long-term = facts saved to a JSON file."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.tools import TOOLS, SCHEMAS, schema
from step03_agent_loop.agent import Agent


class MemoryStore:
    """Long-term memory: a list of facts in a JSON file. Simple, inspectable, deletable."""
    def __init__(self, path="memory.json"):
        self.path = path
        self.facts = json.load(open(path)) if os.path.exists(path) else []

    def save(self, fact):
        if fact not in self.facts:
            self.facts.append(fact)
            json.dump(self.facts, open(self.path, "w"), indent=2)
        return f"saved: {fact}"


class MemoryAgent(Agent):
    def __init__(self, memory_path="memory.json", max_history=12, **kw):
        self.memory = MemoryStore(memory_path)
        tools = dict(TOOLS, save_memory=self.memory.save)
        schemas = SCHEMAS + [schema("save_memory", "Save a lasting fact about the user.",
                                    fact=("string", "The fact to remember"))]
        super().__init__(tools=tools, schemas=schemas, **kw)
        self.history, self.max_history = [], max_history

    def system_prompt(self):
        facts = "\n".join(f"- {f}" for f in self.memory.facts) or "- (nothing yet)"
        return ("You are a helpful agent with memory. Use save_memory for lasting facts.\n"
                f"Known facts about the user:\n{facts}")

    def chat(self, text):
        self.history = self.history[-self.max_history:]   # short-term memory: keep it small
        messages = [{"role": "system", "content": self.system_prompt()}] + self.history
        answer = self.run(text, messages)
        self.history = [m for m in messages if m["role"] != "system"]
        return answer


if __name__ == "__main__":
    a = MemoryAgent()
    print("Chat with memory (Ctrl+C to quit). Try: 'Remember my name is Sahin.'")
    while True:
        print("agent:", a.chat(input("you: ")))

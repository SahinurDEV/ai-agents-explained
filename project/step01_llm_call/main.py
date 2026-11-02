"""Step 1: a plain LLM call. No tools, no memory: text in, text out."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.llm import get_llm

SYSTEM = "You are a friendly assistant. Answer in 2-3 sentences."


def ask(question, llm=None):
    llm = llm or get_llm()
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    return llm.chat(messages).content


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "What is an AI agent, in simple words?"
    print(ask(q))

"""Step 2: tool calling. The model ASKS for a tool; our code RUNS it and sends the result back."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.llm import get_llm
from common.tools import TOOLS, SCHEMAS


def ask_with_tools(question, llm=None, verbose=True):
    llm = llm or get_llm()
    messages = [{"role": "system", "content": "Use tools when they help. Never guess numbers."},
                {"role": "user", "content": question}]
    reply = llm.chat(messages, tools=SCHEMAS)            # 1) model decides
    if not reply.tool_calls:
        return reply.content
    messages.append(reply.as_message())
    for tc in reply.tool_calls:                          # 2) WE execute the tool
        result = TOOLS[tc.name](**tc.arguments)
        if verbose:
            print(f"[tool] {tc.name}({json.dumps(tc.arguments)}) -> {result}")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    return llm.chat(messages, tools=SCHEMAS).content     # 3) model writes the answer


if __name__ == "__main__":
    print(ask_with_tools(" ".join(sys.argv[1:]) or "What is 1234 * 56?"))

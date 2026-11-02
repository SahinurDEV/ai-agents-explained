"""One tiny LLM client used by every step.

Works with any OpenAI-compatible API (OpenAI, Groq, OpenRouter, a local Ollama server ...)
and with an offline MockLLM so you can run everything without a key.

Environment variables (see .env.example):
  LLM_PROVIDER   openai | ollama | mock      (default: openai if OPENAI_API_KEY is set, else mock)
  LLM_BASE_URL   API base URL (Ollama default: http://localhost:11434/v1)
  LLM_API_KEY    your key (Ollama ignores it)
  LLM_MODEL      model name, e.g. gpt-4o-mini or llama3.1
"""
import json
import os
import re
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # dotenv is optional
    pass


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict


@dataclass
class Reply:
    content: str | None
    tool_calls: list = field(default_factory=list)

    def as_message(self):
        """The assistant message to append to the conversation history."""
        msg = {"role": "assistant", "content": self.content or ""}
        if self.tool_calls:
            msg["tool_calls"] = [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)}}
                for tc in self.tool_calls]
        return msg


class OpenAICompatLLM:
    def __init__(self, base_url=None, api_key=None, model=None):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(base_url=base_url, api_key=api_key or "not-needed")

    def chat(self, messages, tools=None, temperature=0.2):
        kw = dict(model=self.model, messages=messages, temperature=temperature)
        if tools:
            kw["tools"] = tools
        m = self.client.chat.completions.create(**kw).choices[0].message
        calls = [ToolCall(tc.id, tc.function.name, json.loads(tc.function.arguments or "{}"))
                 for tc in (m.tool_calls or [])]
        return Reply(m.content, calls)


class MockLLM:
    """A rule-based stand-in for a real model. It is NOT smart; it only exists so the
    code paths (tool calls, loops, memory, RAG, MCP, guardrails) can run offline and in tests."""
    model = "mock"

    def __init__(self):
        self.n = 0

    def _call(self, name, **args):
        self.n += 1
        return Reply(None, [ToolCall(f"call_{self.n}", name, args)])

    def chat(self, messages, tools=None, temperature=0.2):
        tool_names = {t["function"]["name"] for t in (tools or [])}
        last = messages[-1]
        if last["role"] == "tool":
            # Summarise every tool result since the last user message.
            results = []
            for m in reversed(messages):
                if m["role"] == "user":
                    break
                if m["role"] == "tool":
                    results.insert(0, m["content"])
            return Reply("Here is what I found: " + " | ".join(results))
        text = last.get("content") or ""
        low = text.lower()
        already = {tc["function"]["name"] for m in messages if m["role"] == "assistant"
                   for tc in m.get("tool_calls", [])}
        math = re.search(r"(\d[\d\s\.\+\-\*/\(\)]*[\+\-\*/][\d\s\.\+\-\*/\(\)]*\d)", text)
        if "calculator" in tool_names and math:
            return self._call("calculator", expression=math.group(1).strip())
        if "get_weather" in tool_names and "weather" in low:
            city = re.search(r"in ([A-Z][a-zA-Z]+)", text)
            return self._call("get_weather", city=city.group(1) if city else "Dhaka")
        if "save_memory" in tool_names and low.startswith("remember"):
            return self._call("save_memory", fact=text.split(" ", 1)[1].strip(" .:"))
        if "search_docs" in tool_names and "search_docs" not in already and "?" in text:
            return self._call("search_docs", query=text)
        if "add_note" in tool_names and low.startswith("note:"):
            return self._call("add_note", text=text.split(":", 1)[1].strip())
        if "list_notes" in tool_names and "notes" in low and "list_notes" not in already:
            return self._call("list_notes")
        if "send_email" in tool_names and "email" in low:
            return self._call("send_email", to="team@example.com", body=text)
        if "delete_file" in tool_names and "delete" in low:
            return self._call("delete_file", path="notes.txt")
        # Plain answer. Echo memory/context from the system prompt so tests can see it was used.
        system = " ".join(m["content"] for m in messages if m["role"] == "system")
        facts = re.findall(r"- (.+)", system)
        name = next((f for f in facts if "name" in f.lower()), None)
        if "my name" in low and name:
            return Reply(f"(mock) You told me: {name}")
        return Reply(f"(mock) You said: {text}")


def get_llm():
    provider = os.getenv("LLM_PROVIDER") or ("openai" if os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY") else "mock")
    provider = provider.lower()
    if provider == "mock":
        return MockLLM()
    if provider == "ollama":
        return OpenAICompatLLM(os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"), "ollama",
                               os.getenv("LLM_MODEL", "llama3.1"))
    return OpenAICompatLLM(os.getenv("LLM_BASE_URL") or None,
                           os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"),
                           os.getenv("LLM_MODEL", "gpt-4o-mini"))

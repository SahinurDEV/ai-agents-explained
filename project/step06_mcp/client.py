"""Step 6b: an agent that gets its tools from an MCP server instead of hard-coding them.
The agent loop is the same as step 3; only WHERE the tools come from changes."""
import asyncio, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from common.llm import get_llm

SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")


def to_openai_schema(tool):
    """MCP tool description -> OpenAI function-calling schema."""
    return {"type": "function", "function": {"name": tool.name, "description": tool.description or "",
                                             "parameters": tool.input_schema}}


async def run_agent(goal, llm=None, max_steps=6, env=None, verbose=True):
    llm = llm or get_llm()
    params = StdioServerParameters(command=sys.executable, args=[SERVER], env=dict(os.environ, **(env or {})))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [to_openai_schema(t) for t in (await session.list_tools()).tools]
            if verbose:
                print("MCP tools:", [t["function"]["name"] for t in tools])
            messages = [{"role": "system", "content": "You manage the user's notes with the tools."},
                        {"role": "user", "content": goal}]
            for _ in range(max_steps):
                reply = llm.chat(messages, tools=tools)
                messages.append(reply.as_message())
                if not reply.tool_calls:
                    return reply.content
                for tc in reply.tool_calls:
                    res = await session.call_tool(tc.name, tc.arguments)
                    text = "\n".join(c.text for c in res.content if getattr(c, "text", None))
                    if verbose:
                        print(f"[mcp] {tc.name}({json.dumps(tc.arguments)}) -> {text}")
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": text})
            return "Stopped: step limit reached."


if __name__ == "__main__":
    print(asyncio.run(run_agent(" ".join(sys.argv[1:]) or "note: buy milk")))

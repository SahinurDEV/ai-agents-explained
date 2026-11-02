# Step 6 - MCP server and client

**Course link:** Module 4 (MCP) · Section 10 of *AI Agents Explained*

## What you build
`server.py` exposes notes tools over the Model Context Protocol (stdio). `client.py` discovers them at runtime and plugs them into the same agent loop.

## Run it
```bash
cd project
python step06_mcp/client.py "note: finish step 6"
```
No API key? `LLM_PROVIDER=mock` runs offline. Want a free real model? Use Ollama (see `.env.example`).

## Try this
Add a `delete_note` tool to the server. The client needs NO code change - that is the point of MCP. Bonus: connect `server.py` to an MCP host such as Claude Desktop.

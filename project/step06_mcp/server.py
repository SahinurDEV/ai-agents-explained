"""Step 6a: an MCP server exposing a tiny notes app. Any MCP host (Claude Desktop, IDEs,
or our own client.py) can discover and call these tools. Runs over stdio."""
import os
from mcp.server.mcpserver import MCPServer

NOTES_FILE = os.getenv("NOTES_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.txt"))
mcp = MCPServer("notes")


@mcp.tool()
def add_note(text: str) -> str:
    """Add a note to the user's notes file."""
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return f"note added: {text.strip()}"


@mcp.tool()
def list_notes() -> str:
    """List all saved notes."""
    if not os.path.exists(NOTES_FILE):
        return "(no notes yet)"
    return open(NOTES_FILE, encoding="utf-8").read().strip() or "(no notes yet)"


if __name__ == "__main__":
    mcp.run()  # stdio transport

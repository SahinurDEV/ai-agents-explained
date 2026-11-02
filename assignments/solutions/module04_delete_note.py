"""Module 4 solution: add this tool to project/step06_mcp/server.py (below list_notes)."""
# @mcp.tool()
def delete_note(text: str) -> str:
    """Delete every note that matches the given text exactly."""
    import os
    from step06_mcp.server import NOTES_FILE  # inside server.py just use NOTES_FILE
    if not os.path.exists(NOTES_FILE):
        return "(no notes yet)"
    lines = open(NOTES_FILE, encoding="utf-8").read().splitlines()
    keep = [l for l in lines if l.strip() != text.strip()]
    open(NOTES_FILE, "w", encoding="utf-8").write("\n".join(keep) + ("\n" if keep else ""))
    return f"deleted {len(lines) - len(keep)} note(s)"

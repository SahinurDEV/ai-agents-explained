# Module 04 Sample Solution: Build a Mini Knowledge Base

See `solutions/module04_delete_note.py` for the server tool. Typical findings:
- Small chunks (150) retrieve precise lines but lose context; large chunks (600) keep context but bring noise. 300 with overlap is a reasonable start.
- Measure retrieval separately from answer quality: if the right chunk is not retrieved, no prompt can fix the answer.
- The client discovers `delete_note` automatically via `list_tools()` - this is the main benefit of MCP.

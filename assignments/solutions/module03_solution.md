# Module 03 Sample Solution: Add a Tool and a Memory

See `solutions/module03_get_time.py`. Key points:
- The schema describes *when* to use the tool ("Get the current local time for a city"), not just its name.
- Unknown cities return `"error: unknown city ..."` as a string; the loop passes it back and the model can ask the user or try another spelling.
- Memory: `MemoryAgent.chat("Remember I prefer Celsius")` writes to `memory.json`; a new `MemoryAgent` reads it into the system prompt.

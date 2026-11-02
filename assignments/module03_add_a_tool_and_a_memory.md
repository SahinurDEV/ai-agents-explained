# Module 03 Assignment: Add a Tool and a Memory

*Course module: Tools, APIs, Memory and State (Udemy Section 4)* · Time: 30-90 min

## Your task
Code track (uses `project/`):
1. In `common/tools.py` add `get_time(city: str) -> str` (use `zoneinfo`) and its JSON schema.
2. Run `step03_agent_loop/agent.py "What time is it in Tokyo?"` with Ollama or an API key and check the trace.
3. Make the tool fail for an unknown city and confirm the agent recovers (error becomes an observation).
4. In step 4, save one preference and show it is used in a new session.
No-code track: write the JSON schema for 3 tools of your Module 2 agent, including required fields, and describe what the agent should do when each tool fails.

## What to submit
Your code diff (or the schemas) + a screenshot/log of a run.

## Check yourself
- Did you connect your answer to the concepts of Module 3?
- Could someone else repeat your steps from what you wrote?

Sample solution: `solutions/module03_solution.md`

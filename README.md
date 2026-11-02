# AI Agents Explained - Companion Repo

Code, assignments and cheat sheets for the Udemy course **AI Agents Explained: Fundamentals, Architecture, RAG & MCP**.

Learn the concepts in the videos, then build them here: a working AI agent in Python with tool calling, an agent loop, memory, RAG (Chroma), an MCP server/client and guardrails. Runs **offline** (mock model), **free** (Ollama), or with any OpenAI-compatible API.

## What's inside
| Folder | What | Course |
|---|---|---|
| [project/](project) | 7-step hands-on project: build your own agent | Section 10 |
| [assignments/](assignments) | One practice assignment per module + sample solutions | Sections 2-9 |
| [cheatsheets/](cheatsheets) | Prompt templates, agent design checklist, MCP setup guide, RAG checklist (MD + PDF) | All |

## Course map
| Module | Topic | Assignment | Project step |
|---|---|---|---|
| 01 | AI and LLM Foundations | [Spot the Hallucination](assignments/module01_spot_the_hallucination.md) | step01 |
| 02 | Understanding AI Agents | [Design an Agent on One Page](assignments/module02_design_an_agent_on_one_page.md) | step03 |
| 03 | Tools, APIs, Memory and State | [Add a Tool and a Memory](assignments/module03_add_a_tool_and_a_memory.md) | step02, step04 |
| 04 | Knowledge, RAG and MCP | [Build a Mini Knowledge Base](assignments/module04_build_a_mini_knowledge_base.md) | step05, step06 |
| 05 | Workflows and Multi-Agent Systems | [Workflow or Agent?](assignments/module05_workflow_or_agent.md) | - |
| 06 | Real-World Applications | [Use-Case Teardown](assignments/module06_use-case_teardown.md) | - |
| 07 | Security, Evaluation and Production | [Red-Team Your Agent](assignments/module07_red-team_your_agent.md) | step07 |
| 08 | Final Review and Next Steps | [Capstone: Your Own Agent](assignments/module08_capstone_your_own_agent.md) | all |

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cd project && bash smoke.sh && pytest -q tests
```
Requires Python 3.10+. Details: [project/README.md](project/README.md).

## License
MIT - see [LICENSE](LICENSE). Example data in `project/step05_rag/docs` is fictional.

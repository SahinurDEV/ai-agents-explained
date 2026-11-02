# Module 01 Sample Solution: Spot the Hallucination

**Sample table**

| Question | Verdict | Cause | Fix |
|---|---|---|---|
| Capital of Australia | correct | - | - |
| 48,213 x 7,906 | often wrong in the last digits | token prediction, not arithmetic | calculator tool |
| Yesterday's football score | wrong / refuses | training cut-off, no live data | search/API tool |
| Founding year of a small town | confidently wrong | rare fact, hallucination | retrieval from a trusted source |
| Who wrote Hamlet | correct | - | - |

**Reflection.** Arithmetic and live data are fixed by *tools* (calculator, API). Rare or private facts are fixed by *retrieval* (RAG) with citations so they can be checked. Hallucination never fully disappears, which is why answers should carry sources and important claims need verification.

# RAG Checklist

## Data
- [ ] Sources listed, owned, and up to date; stale docs removed
- [ ] Clean text (no headers/footers/nav noise); tables handled
- [ ] Metadata kept: source, title, date, access level

## Chunking
- [ ] Start ~300-800 characters (or 200-500 tokens) with 10-20% overlap
- [ ] Split on headings/paragraphs, not mid-sentence
- [ ] Each chunk understandable on its own (prepend the title)

## Embedding & storage
- [ ] One embedding model for both documents and queries
- [ ] Vector DB chosen (Chroma locally; pgvector, Qdrant, etc. in production)
- [ ] Re-index on document changes; track versions

## Retrieval
- [ ] Top-k tuned (start k=3-5); similarity threshold
- [ ] Hybrid search (keywords + vectors) for names, codes, IDs
- [ ] Optional re-ranker; metadata filters (permissions!)

## Generation
- [ ] "Answer only from context, else say I don't know"
- [ ] Citations [source] on every fact
- [ ] Context fits the window with room for the answer

## Evaluation
- [ ] 20+ questions with expected source and answer
- [ ] Measure retrieval hit rate separately from answer correctness
- [ ] Check faithfulness (no claims beyond the context)
- [ ] Re-run after every change to chunking, model or prompt

## Security
- [ ] Users only retrieve documents they may access
- [ ] Retrieved text is data, not instructions (indirect prompt injection)

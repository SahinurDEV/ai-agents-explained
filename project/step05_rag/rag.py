"""Step 5: RAG. Chunk docs -> embed -> store in Chroma -> retrieve -> answer WITH sources.

Embeddings: EMBED_PROVIDER=openai uses the API (text-embedding-3-small);
anything else uses a tiny offline 'hashing' embedder so the project runs with no key.
(The offline embedder only matches words, not meaning. Real embeddings are much better.)
"""
import glob, hashlib, math, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import chromadb
from common.tools import TOOLS, SCHEMAS, schema
from step03_agent_loop.agent import Agent

HERE = os.path.dirname(os.path.abspath(__file__))


class HashEmbedder:
    """Offline bag-of-words embedder (384 dims). Good enough to demo retrieval."""
    def embed(self, texts):
        out = []
        for t in texts:
            v = [0.0] * 384
            for w in re.findall(r"[a-z0-9]+", t.lower()):
                if len(w) > 2:
                    v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 384] += 1.0
            n = math.sqrt(sum(x * x for x in v)) or 1.0
            out.append([x / n for x in v])
        return out


class OpenAIEmbedder:
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(base_url=os.getenv("LLM_BASE_URL") or None,
                             api_key=os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("EMBED_MODEL", "text-embedding-3-small")

    def embed(self, texts):
        return [d.embedding for d in self.client.embeddings.create(model=self.model, input=texts).data]


def get_embedder():
    return OpenAIEmbedder() if os.getenv("EMBED_PROVIDER", "local") == "openai" else HashEmbedder()


def chunk(text, size=300, overlap=50):
    """Split text into overlapping character chunks, on line boundaries where possible."""
    chunks, cur = [], ""
    for line in text.splitlines():
        if len(cur) + len(line) > size and cur:
            chunks.append(cur.strip())
            cur = cur[-overlap:]
        cur += line + "\n"
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


class KnowledgeBase:
    def __init__(self, path=None, embedder=None):
        client = chromadb.PersistentClient(path=path) if path else chromadb.EphemeralClient()
        self.col = client.get_or_create_collection("docs", metadata={"hnsw:space": "cosine"})
        self.embedder = embedder or get_embedder()

    def ingest(self, folder=os.path.join(HERE, "docs")):
        ids, docs, metas = [], [], []
        for f in sorted(glob.glob(os.path.join(folder, "*.md"))):
            for i, c in enumerate(chunk(open(f, encoding="utf-8").read())):
                ids.append(f"{os.path.basename(f)}#{i}"); docs.append(c)
                metas.append({"source": os.path.basename(f)})
        self.col.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=self.embedder.embed(docs))
        return len(ids)

    def search(self, query, k=2):
        r = self.col.query(query_embeddings=self.embedder.embed([query]), n_results=k)
        return [(m["source"], d) for m, d in zip(r["metadatas"][0], r["documents"][0])]

    def search_docs(self, query):
        """Tool version: returns text with [source] tags the model must cite."""
        return "\n".join(f"[{s}] {d}" for s, d in self.search(query))


def rag_agent(kb, **kw):
    tools = dict(TOOLS, search_docs=kb.search_docs)
    schemas = SCHEMAS + [schema("search_docs", "Search the company documents. Use for any policy question.",
                                query=("string", "What to look for"))]
    a = Agent(tools=tools, schemas=schemas, **kw)
    return a


if __name__ == "__main__":
    kb = KnowledgeBase(path=os.path.join(HERE, ".chroma"))
    print("indexed chunks:", kb.ingest())
    q = " ".join(sys.argv[1:]) or "How long do I have to ask for a refund?"
    print(rag_agent(kb).run(q + " Cite the [source]."))

from ingestion.connectors import load_all_sources
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_texts

from retrieval.vector_store import VectorStore
from retrieval.bm25 import BM25Retriever
from retrieval.hybrid_search import hybrid_search
from retrieval.reranker import simple_rerank

from agent.router import route_query
from agent.tools import web_search, calculator_tool, tool_selector
from agent.validator import validate_answer

from knowledge_graph.kg_query import enrich_with_kg

from llm.generator import generate_answer

from utils.logger import log
from utils.helpers import format_context


# ---------------------------
# 🔧 QUERY REWRITE (LLM)
# ---------------------------
def rewrite_query(query):
    prompt = f"""
Convert this question into SHORT search keywords.

Return ONLY keywords.

Question:
{query}

Keywords:
"""
    try:
        rewritten = generate_answer(prompt)
        rewritten = rewritten.lower().replace("\n", " ")
        return " ".join(rewritten.split()[:8])
    except:
        return query


# ---------------------------
# 🔹 Load data
# ---------------------------
docs = load_all_sources()
chunks = [c for doc in docs for c in chunk_text(doc)]

log(f"Loaded {len(chunks)} chunks")

# ---------------------------
# 🔹 Embeddings
# ---------------------------
embeddings = embed_texts(chunks)

vector_store = VectorStore(len(embeddings[0]))
vector_store.add(embeddings, chunks)

bm25 = BM25Retriever(chunks)


# ---------------------------
# 🧠 MAIN QUERY
# ---------------------------
def run_query(query):
    log(f"Query: {query}")

    # 🔥 Dual Query (NO HARDCODING)
    search_query_1 = query
    search_query_2 = rewrite_query(query)

    # 🔹 Tool selection
    tool = tool_selector(query)

    if tool == "calculator":
        return calculator_tool(query)

    route = route_query(query)

    if route == "web":
        context_chunks = web_search(query)
    else:
        # 🔥 Run both searches
        results_1 = hybrid_search(search_query_1, vector_store, bm25, embed_texts)
        results_2 = hybrid_search(search_query_2, vector_store, bm25, embed_texts)

        # 🔥 Merge results
        combined = results_1 + results_2
        seen = set()
        results = []

        for r in combined:
            if r not in seen:
                results.append(r)
                seen.add(r)

        # 🔥 Rerank
        results = simple_rerank(query, results)

        context_chunks = enrich_with_kg(results)

    # 🔥 Remove noisy chunks
    context_chunks = [c for c in context_chunks if len(c.split()) > 20]

    context = format_context(context_chunks)

    # ---------------------------
    # 🧠 FINAL PROMPT
    # ---------------------------
    prompt = f"""
You are a data extraction expert.

The context may come from messy PDF text, tables, or charts.

Rules:
- Extract ONLY clearly matchable values
- If unclear → skip it (DO NOT guess)
- Return structured answer (table or bullets)
- Do NOT output raw messy text

Context:
{context}

Question:
{query}

Answer:
"""

    answer = generate_answer(prompt)

    if not validate_answer(answer):
        log("Validation failed", "WARN")
        return "Answer not reliable. Try refining."

    return answer


# ---------------------------
# CLI TEST
# ---------------------------
if __name__ == "__main__":
    while True:
        q = input("Ask: ")
        print(run_query(q))

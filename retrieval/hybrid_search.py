#####################correct
def hybrid_search(query, vector_store, bm25, embed_fn=None, k=20):
    print("\n🧠 [HYBRID SEARCH] Running...")

    # 🔹 BM25 (fast keyword)
    sparse_results = bm25.search(query, k=k)
    print(f"🔎 BM25 returned: {len(sparse_results)}")

    # 🔹 Dense (semantic)
    dense_results = []
    if embed_fn:
        query_embedding = embed_fn([query])[0]
        dense_results = vector_store.search(query_embedding, k=k)
        print(f"🧬 Dense returned: {len(dense_results)}")

    # 🔹 Merge with scoring
    scores = {}

    for i, doc in enumerate(sparse_results):
        scores[doc] = scores.get(doc, 0) + (k - i)

    for i, doc in enumerate(dense_results):
        scores[doc] = scores.get(doc, 0) + (k - i) * 0.8

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    final = [doc for doc, _ in ranked]

    print(f"✅ Final results: {len(final)}")

    return final


###############################check
# def safe_text(doc):
#     if isinstance(doc, dict):
#         return doc.get("text", "")
#     return doc


# def safe_type(doc):
#     if isinstance(doc, dict):
#         return doc.get("type", "text")
#     return "text"


# def hybrid_search(query, vector_store, bm25, embed_fn, k=8):

#     print("\n🔍 Hybrid search started")

#     sparse = bm25.search(query, k=k)

#     query_embedding = embed_fn([query])[0]
#     dense = vector_store.search(query_embedding, k=k)

#     scores = {}

#     def boost(doc):
#         q = query.lower()

#         if any(word in q for word in ["value", "total", "data", "table"]):
#             if safe_type(doc) == "table":
#                 return 2
#         return 1

#     # -------------------------
#     # BM25 scoring (strings or dicts safe)
#     # -------------------------
#     for i, doc in enumerate(sparse):
#         text = safe_text(doc)
#         scores[text] = scores.get(text, 0) + (k - i) * boost(doc)

#     # -------------------------
#     # Dense scoring
#     # -------------------------
#     for i, doc in enumerate(dense):
#         text = safe_text(doc)
#         scores[text] = scores.get(text, 0) + (k - i) * 0.7 * boost(doc)

#     # -------------------------
#     # Ranking
#     # -------------------------
#     ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

#     results = []
#     seen = set()

#     # rebuild structured results safely
#     all_docs = sparse + dense

#     for text, _ in ranked:
#         for d in all_docs:
#             if safe_text(d) == text and text not in seen:
#                 if isinstance(d, dict):
#                     results.append(d)
#                 else:
#                     results.append({"text": d, "type": "text"})
#                 seen.add(text)
#                 break

#     print(f"✅ Retrieved {len(results)} docs")

#     return results[:k]
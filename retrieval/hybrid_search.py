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



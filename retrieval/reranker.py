def simple_rerank(query, docs):
    print("\n🧠 [RERANK] Running...")

    q_words = set(query.lower().split())

    def score(doc):
        doc_lower = doc.lower()

        # keyword overlap
        overlap = sum(1 for w in q_words if w in doc_lower)

        # numeric density (IMPORTANT for tables)
        numbers = sum(1 for c in doc if c.isdigit())

        # length bonus (avoid tiny chunks)
        length_bonus = min(len(doc.split()) / 200, 1)

        return overlap * 2 + numbers * 0.01 + length_bonus

    ranked = sorted(docs, key=score, reverse=True)

    print("✅ Rerank complete")

    return ranked

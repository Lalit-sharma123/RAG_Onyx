from knowledge_graph.kg_builder import graph

def get_related_nodes(entity, depth=1):
    if entity not in graph:
        return []

    neighbors = list(graph.neighbors(entity))
    return neighbors[:depth]


def enrich_with_kg(context_chunks):
    enriched = []

    for chunk in context_chunks:
        words = chunk.split()
        related_info = []

        for word in words[:5]:  # simple heuristic
            related = get_related_nodes(word)
            if related:
                related_info.append(f"{word} -> {related}")

        enriched.append(chunk + "\nKG: " + ", ".join(related_info))

    return enriched
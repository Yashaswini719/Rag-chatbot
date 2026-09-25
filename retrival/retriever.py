from retrival.hybrid_search import hybrid_search


def retrieve(query: str, top_k: int = 5):
    return hybrid_search(query, top_k)
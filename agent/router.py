def route_query(query):
    if "latest" in query or "news" in query:
        return "web"
    return "internal"
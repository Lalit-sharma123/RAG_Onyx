def web_search(query):
    return [f"[WEB] Result for: {query}"]


def calculator_tool(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid calculation"


def tool_selector(query):
    q = query.lower()

    # if any(op in q for op in ["+", "-", "*", "/"]):
    #     return "calculator"
    if any(op in q for op in ["+", "-", "*", "/"]) and any(c.isdigit() for c in q):
        return "calculator"
    elif "latest" in q or "news" in q:
        return "web"

    return "none"
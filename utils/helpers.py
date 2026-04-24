def clean_text(text):
    return text.strip().replace("\n", " ")


def deduplicate_chunks(chunks):
    return list(set(chunks))


def format_context(chunks, max_chars=2000):
    context = ""
    for chunk in chunks:
        if len(context) + len(chunk) < max_chars:
            context += chunk + "\n"
        else:
            break
    return context
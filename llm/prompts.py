def build_rag_prompt(query, context):
    return f"""
You are an AI assistant.

The context may contain district-wise data.

Extract specific numbers if present.

If exact answer not found, summarize best possible.

Context:
{context}

Question:
{query}

Answer:
"""



# def build_rag_prompt(query, context):
#     return f"""
# You are an AI assistant.

# Use ONLY the provided context to answer the question.

# Instructions:
# - Carefully read the context before answering.
# - If the answer contains numbers, extract them accurately.
# - If the answer is descriptive, summarize clearly.
# - If multiple pieces of information are present, combine them logically.
# - If the answer is not found in the context, say: "I don't know".

# Context:
# {context}

# Question:
# {query}

# Answer:
# """



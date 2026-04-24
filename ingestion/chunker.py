##################correct
def chunk_text(text, max_words=300, overlap=50):
    print("\n🔵 [CHUNKING] Running...")

    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words - overlap):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    print(f"✅ Total chunks created: {len(chunks)}")

    return chunks




##############################check
# def chunk_documents(docs, chunk_size=300, overlap=80):
#     print("\n🔵 Chunking structured documents...")

#     chunks = []

#     for doc in docs:
#         words = doc["text"].split()

#         for i in range(0, len(words), chunk_size - overlap):
#             chunk_text = " ".join(words[i:i + chunk_size])

#             chunks.append({
#                 "text": chunk_text,
#                 "page": doc["page"],
#                 "type": doc["type"],
#                 "source": doc["source"]
#             })

#     print(f"✅ Total chunks: {len(chunks)}")
#     return chunks
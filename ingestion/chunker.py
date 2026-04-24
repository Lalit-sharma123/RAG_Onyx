def chunk_text(text, max_words=300, overlap=50):
    print("\n🔵 [CHUNKING] Running...")

    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words - overlap):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    print(f"✅ Total chunks created: {len(chunks)}")

    return chunks





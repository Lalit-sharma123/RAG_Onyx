#########################correct

import streamlit as st
import tempfile

from ingestion.chunker import chunk_text
from ingestion.embedder import embed_texts
from retrieval.vector_store import VectorStore
from retrieval.bm25 import BM25Retriever
from retrieval.hybrid_search import hybrid_search
from retrieval.reranker import simple_rerank

from llm.generator import stream_answer
from utils.pdf_vision import extract_text_with_ocr


# ---------------------------
# UI CONFIG
# ---------------------------
st.set_page_config(page_title="Document Q&A", page_icon="📄")
st.title("📄 Upload → Ask → Get structured answers")


# ---------------------------
# SESSION STATE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "bm25" not in st.session_state:
    st.session_state.bm25 = None


# ---------------------------
# CACHE INDEX
# ---------------------------
@st.cache_resource
def build_index(text):
    print("\n🔵 [INDEX] Chunking started...")

    chunks = chunk_text(text)
    print(f"✅ Total chunks: {len(chunks)}")

    embeddings = embed_texts(chunks)
    print("✅ Embeddings created")

    vector_store = VectorStore(len(embeddings[0]))
    vector_store.add(embeddings, chunks)
    print("✅ Vector store ready")

    bm25 = BM25Retriever(chunks)
    print("✅ BM25 ready")

    return vector_store, bm25


# ---------------------------
# CONTEXT LIMIT
# ---------------------------
def limit_context(text, max_chars=4000):
    return text[:max_chars]


# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

print("\n🟡 Waiting for file upload...")

if uploaded_file:

    print("\n🟢 File uploaded")

    with st.spinner("Processing document..."):

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        print("📄 Extracting text...")
        full_text = extract_text_with_ocr(file_path)

        print("✅ Text extracted")
        print(f"📏 Text length: {len(full_text)}")

        vector_store, bm25 = build_index(full_text)

        st.session_state.vector_store = vector_store
        st.session_state.bm25 = bm25

        st.success("✅ Document processed!")


# ---------------------------
# CHAT HISTORY
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------------------
# ASK QUESTION
# ---------------------------
query = st.chat_input("Ask a question...")
print("Ask query")

if query:

    print("\n🟣 NEW QUERY")
    print("🔍 Query:", query)

    if not st.session_state.vector_store:
        st.warning("⚠️ Upload a PDF first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        vector_store = st.session_state.vector_store
        bm25 = st.session_state.bm25

        with st.spinner("Thinking..."):

            # ---------------------------
            # 🔍 RETRIEVAL
            # ---------------------------
            print("\n🔵 Running hybrid search...")
            results = hybrid_search(query, vector_store, bm25, embed_texts, k=30)

            print(f"✅ Retrieved: {len(results)} chunks")

            print("\n🟠 TOP 3 RAW RESULTS:")
            for i, r in enumerate(results[:3]):
                print(f"\n--- Chunk {i} ---\n{r[:300]}")

            # ---------------------------
            # 🔁 RERANK
            # ---------------------------
            results = simple_rerank(query, results)

            print("\n🟢 AFTER RERANK (Top 3):")
            for i, r in enumerate(results[:3]):
                print(f"\n--- Chunk {i} ---\n{r[:300]}")

            # ---------------------------
            # 🧠 CONTEXT SELECTION (GENERIC)
            # ---------------------------
            print("\n🧠 Selecting best chunks...")

            context_chunks = []

            for chunk in results:
                words = chunk.split()

                # skip noise
                if len(words) < 40:
                    continue

                # prefer numeric/table chunks
                numeric_score = sum(1 for c in chunk if c.isdigit())

                context_chunks = results[:8]

                if len(context_chunks) >= 6:
                    break

            # fallback
            if not context_chunks:
                context_chunks = results[:6]

            print(f"✅ Selected {len(context_chunks)} chunks")

            for i, c in enumerate(context_chunks):
                print(f"\n=== CONTEXT {i} ===\n{c[:400]}")

            # ---------------------------
            # FINAL CONTEXT
            # ---------------------------
            context = "\n\n".join(context_chunks)
            context = limit_context(context)

            print("\n📦 FINAL CONTEXT LENGTH:", len(context))
            print("\n📦 CONTEXT PREVIEW:\n", context[:1000])

            # ---------------------------
            # 🧠 BEST PROMPT (GENERIC)
            # ---------------------------
            prompt = f"""
You are a precise data extraction assistant.

Instructions:
- Use ONLY the given context
- Do NOT guess
- Extract exact values if present
- If multiple values exist, list them clearly
- If total is asked and values are present, compute correctly
- If answer not found, say: Not found

Context:
{context}

Question:
{query}

Answer:
"""

            print("\n🚀 Sending to LLM...")

            # ---------------------------
            # STREAM RESPONSE
            # ---------------------------
            response_box = st.empty()
            full_answer = ""

            for chunk in stream_answer(prompt):
                if isinstance(chunk, str):
                    full_answer += chunk
                    response_box.markdown(full_answer + "▌")

            response_box.markdown(full_answer)

            print("\n✅ FINAL ANSWER:")
            print(full_answer)

            answer = full_answer

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })






#################################check
# import streamlit as st
# import tempfile

# from ingestion.loader import load_pdf   # structured loader
# from ingestion.chunker import chunk_documents
# from ingestion.embedder import embed_texts

# from retrieval.vector_store import VectorStore
# from retrieval.bm25 import BM25Retriever
# from retrieval.hybrid_search import hybrid_search

# from llm.generator import stream_answer
# from utils.pdf_vision import extract_text_with_ocr


# # ---------------------------
# # UI CONFIG
# # ---------------------------
# st.set_page_config(page_title="Document Q&A", page_icon="📄")
# st.title("📄 Upload → Ask → Get structured answers")


# # ---------------------------
# # SESSION STATE
# # ---------------------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vector_store" not in st.session_state:
#     st.session_state.vector_store = None

# if "bm25" not in st.session_state:
#     st.session_state.bm25 = None


# # ---------------------------
# # CACHE INDEX (STRUCTURED)
# # ---------------------------
# @st.cache_resource
# def build_index(docs):

#     print("\n🔵 [INDEX] Structured chunking started...")

#     chunks = chunk_documents(docs)
#     print(f"✅ Total chunks: {len(chunks)}")

#     texts = [c["text"] for c in chunks]

#     print("🧠 Creating embeddings...")
#     embeddings = embed_texts(texts)
#     print("✅ Embeddings created")

#     vector_store = VectorStore(len(embeddings[0]))
#     vector_store.add(embeddings, chunks)
#     print("📦 Stored chunks in FAISS")

#     # 🔥 FIX HERE
#     bm25 = BM25Retriever(texts)
#     print("✅ BM25 ready")

#     return vector_store, bm25


# # ---------------------------
# # CONTEXT LIMIT
# # ---------------------------
# def limit_context(text, max_chars=4000):
#     return text[:max_chars]


# # ---------------------------
# # FILE UPLOAD
# # ---------------------------
# uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# print("\n🟡 Waiting for file upload...")

# if uploaded_file:

#     print("\n🟢 File uploaded")

#     with st.spinner("Processing document..."):

#         with tempfile.NamedTemporaryFile(delete=False) as tmp:
#             tmp.write(uploaded_file.read())
#             file_path = tmp.name

#         # ---------------------------
#         # STRUCTURED LOADING
#         # ---------------------------
#         print("📄 Loading structured PDF (text + tables)...")
#         docs = load_pdf(file_path)

#         # ---------------------------
#         # OCR FOR IMAGES / GRAPHS
#         # ---------------------------
#         print("🧠 Running OCR for images...")
#         ocr_text = extract_text_with_ocr(file_path)

#         docs.append({
#             "text": ocr_text,
#             "page": None,
#             "type": "ocr",
#             "source": file_path
#         })

#         print(f"📦 Total documents (with OCR): {len(docs)}")

#         # ---------------------------
#         # BUILD INDEX
#         # ---------------------------
#         vector_store, bm25 = build_index(docs)

#         st.session_state.vector_store = vector_store
#         st.session_state.bm25 = bm25

#         st.success("✅ Document processed!")


# # ---------------------------
# # CHAT HISTORY
# # ---------------------------
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])


# # ---------------------------
# # ASK QUESTION
# # ---------------------------
# query = st.chat_input("Ask a question...")
# print("🟣 Waiting for query...")

# if query:

#     print("\n🟣 NEW QUERY")
#     print("🔍 Query:", query)

#     if not st.session_state.vector_store:
#         st.warning("⚠️ Upload a PDF first.")
#         st.stop()

#     st.session_state.messages.append({"role": "user", "content": query})

#     with st.chat_message("user"):
#         st.markdown(query)

#     with st.chat_message("assistant"):

#         vector_store = st.session_state.vector_store
#         bm25 = st.session_state.bm25

#         with st.spinner("Thinking..."):

#             # ---------------------------
#             # 🔍 RETRIEVAL
#             # ---------------------------
#             print("\n🔵 Running hybrid search...")
#             results = hybrid_search(query, vector_store, bm25, embed_texts, k=20)

#             print(f"✅ Retrieved: {len(results)} chunks")

#             print("\n🟠 TOP 3 RESULTS:")
#             for i, r in enumerate(results[:3]):
#                 print(f"\n--- Chunk {i} ---\n{r['text'][:300]}")

#             # ---------------------------
#             # 🧠 CONTEXT SELECTION
#             # ---------------------------
#             print("\n🧠 Selecting structured chunks...")

#             context_chunks = results[:8]

#             for i, c in enumerate(context_chunks):
#                 print(f"\n=== CONTEXT {i} ===\n{c['text'][:400]}")

#             # ---------------------------
#             # FINAL CONTEXT (WITH METADATA)
#             # ---------------------------
#             context = ""

#             for c in context_chunks:
#                 context += f"""
# [Page {c.get('page')}] ({c.get('type')})
# {c['text']}
# ----------------
# """

#             context = limit_context(context)

#             print("\n📦 FINAL CONTEXT LENGTH:", len(context))
#             print("\n📦 CONTEXT PREVIEW:\n", context[:1000])

#             # ---------------------------
#             # 🧠 PROMPT
#             # ---------------------------
#             prompt = f"""
# You are an expert document analyst.

# Rules:
# - Use table data if present
# - Prefer structured data
# - Always mention page number
# - Do not guess
# - If not found → say "Not found"

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#             print("\n🚀 Sending to LLM...")

#             # ---------------------------
#             # STREAM RESPONSE
#             # ---------------------------
#             response_box = st.empty()
#             full_answer = ""

#             for chunk in stream_answer(prompt):
#                 if isinstance(chunk, str):
#                     full_answer += chunk
#                     response_box.markdown(full_answer + "▌")

#             response_box.markdown(full_answer)

#             print("\n✅ FINAL ANSWER:")
#             print(full_answer)

#             answer = full_answer

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": answer
#         })
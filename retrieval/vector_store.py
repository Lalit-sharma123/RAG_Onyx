#########################################correct
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)

    def search(self, query_embedding, k=5):
        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )
        return [self.texts[i] for i in I[0]]
    
    


###################check
# import faiss
# import numpy as np
# class VectorStore:
#     def __init__(self, dim):
#         self.index = faiss.IndexFlatL2(dim)
#         self.data = []

#     def add(self, embeddings, docs):
#         self.index.add(np.array(embeddings).astype("float32"))
#         self.data.extend(docs)

#         print(f"📦 Stored {len(self.data)} chunks")

#     def search(self, query_embedding, k=5):
#         D, I = self.index.search(
#             np.array([query_embedding]).astype("float32"), k
#         )

#         return [self.data[i] for i in I[0]]
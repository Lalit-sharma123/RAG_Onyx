# from rank_bm25 import BM25Okapi

# class BM25Retriever:
#     def __init__(self, docs):
#         self.tokenized = [doc.split() for doc in docs]
#         self.bm25 = BM25Okapi(self.tokenized)
#         self.docs = docs

#     def search(self, query, k=5):
#         scores = self.bm25.get_scores(query.split())
#         top_k = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
#         return [self.docs[i] for i in top_k]


###########################
import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return text.split()


class BM25Retriever:
    def __init__(self, docs):
        self.tokenized = [tokenize(doc) for doc in docs]
        self.bm25 = BM25Okapi(self.tokenized)
        self.docs = docs

    def search(self, query, k=5):
        tokenized_query = tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_k = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.docs[i] for i in top_k]
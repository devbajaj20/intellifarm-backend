from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("rag/knowledge.txt", "r", encoding="utf-8") as f:
    docs = [line.strip() for line in f if line.strip()]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)


def ask_rag(query):
    q = vectorizer.transform([query])
    scores = cosine_similarity(q, X)[0]

    best_idx = scores.argmax()
    best_score = scores[best_idx]

    if best_score < 0.15:
        return "I don't have enough information on that yet."

    return docs[best_idx]
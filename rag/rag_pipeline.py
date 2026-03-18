from config.Settings import (
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    SIMILARITY_THRESHOLD,
    TOP_K
)

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# LOAD EMBEDDING MODEL
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# LOAD FAISS VECTOR DATABASE
vector_db = FAISS.load_local(
    FAISS_INDEX_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


# RETRIEVE DOCUMENTS
def retrieve_documents(query: str):
    results = vector_db.similarity_search_with_score(query, k=TOP_K)

    return [
        {
            "content": doc.page_content,
            "score": float(score)
        }
        for doc, score in results
    ]


# BUILD CONTEXT (TOP RESULT ONLY)
def build_context(docs):
    return docs[0]["content"]


# EXTRACT ANSWER
def generate_answer(context: str):
    if "?" in context:
        return context.split("?", 1)[1].strip()
    return context.strip()


# MAIN RAG PIPELINE
def ask_question(query: str):
    results = retrieve_documents(query)

    best_score = results[0]["score"]

    # 🔒 Hallucination blocking
    if best_score > SIMILARITY_THRESHOLD:
        return {
            "query": query,
            "answer": "I don't know based on the provided context.",
            "retrieved_documents": results
        }

    context = build_context(results)

    answer = generate_answer(context)

    return {
        "query": query,
        "answer": answer,
        "retrieved_documents": results
    }


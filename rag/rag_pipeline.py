from config.Settings import (
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    SIMILARITY_THRESHOLD,
    TOP_K
)

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

vector_db = None


def load_vector_db():
    global vector_db

    if vector_db is None:
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        vector_db = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    return vector_db


def get_llm():
    llm_base = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        temperature=0.3,
        max_new_tokens=40,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        timeout=10
    )

    return ChatHuggingFace(llm=llm_base)


def generate_specs_pipeline(requirement: str):
    llm = get_llm()
    requirement = requirement[:200]

    prompt = f"""
Extract key features, user actions, API endpoints, and database tables.

Requirement:
{requirement}

Give output in this format:

Features:
- ...

User Stories:
- As a user, I can ...

API Endpoints:
- METHOD /path

Database:
- table_name(columns)
"""

    try:
        response = llm.invoke(prompt).content
        return {"output": response}

    except Exception as e:
        print("SPEC ERROR:", e)
        return {
            "output": "Server busy, please try again in few seconds"
        }


# RETRIEVE DOCUMENTS
def retrieve_documents(query: str):
    db = load_vector_db()
    results = db.similarity_search_with_score(query, k=TOP_K)

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
def generate_answer(query: str, context: str):
    llm = get_llm()
    prompt = f"""
You are an AI assistant.

Answer the user's question ONLY using the given context.

If the answer is not in the context, say:
"I don't know based on the provided context."

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = llm.invoke(prompt).content
        return response.strip()

    except Exception as e:
        print("ANSWER ERROR:", e)
        return "Server busy, please try again"


# MAIN RAG PIPELINE
def ask_question(query: str):
    results = retrieve_documents(query)

    best_score = results[0]["score"]

    # Hallucination blocking
    if best_score > SIMILARITY_THRESHOLD:
        return {
            "query": query,
            "answer": "I don't know based on the provided context.",
            "retrieved_documents": results
        }

    context = build_context(results)

    answer = generate_answer(query, context)

    return {
        "query": query,
        "answer": answer,
        "retrieved_documents": results
    }

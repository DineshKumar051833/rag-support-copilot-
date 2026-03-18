# 🧠 RAG Support Copilot

A production-ready **Retrieval-Augmented Generation (RAG)** based support assistant built using **FastAPI, FAISS, and Hugging Face embeddings**.

This application answers user queries strictly based on provided documentation, ensuring **zero hallucination** and high accuracy.

---

## 🚀 Live Demo

🔗 https://dinesh-05-rag-support-copilot.hf.space/docs

---

## 📌 Features

* ✅ Accurate FAQ-based question answering
* ✅ Zero hallucination (strict retrieval-based response)
* ✅ FastAPI backend with REST API
* ✅ FAISS vector database for similarity search
* ✅ Hugging Face sentence-transformer embeddings
* ✅ Session-based authentication (Signup/Login)
* ✅ Deployed on Hugging Face Spaces (Docker)

---

## 🏗️ Architecture

```
User Query
    ↓
FAISS Vector Search (Top-K)
    ↓
Best Matching Document
    ↓
Answer Extraction (No Hallucination)
    ↓
Response
```

---

## 🧠 Tech Stack

| Component  | Technology                               |
| ---------- | ---------------------------------------- |
| Backend    | FastAPI                                  |
| Vector DB  | FAISS                                    |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Framework  | LangChain                                |
| Deployment | Hugging Face Spaces (Docker)             |
| Auth       | Session-based (Starlette Middleware)     |

---

## ⚙️ How It Works

1. User sends a query via API
2. Query is converted into embeddings
3. FAISS retrieves top relevant documents
4. Best match is selected using similarity score
5. Answer is extracted directly from context
6. If confidence is low → returns fallback response

---

## 🛡️ Hallucination Prevention

This system **does NOT rely on LLM generation** for answers.

* ✔ Uses strict retrieval-based extraction
* ✔ Applies similarity threshold filtering
* ✔ Returns:

  ```
  "I don't know based on the provided context."
  ```

  when no relevant data is found

---

## 📡 API Endpoints

### 🔹 Ask Question

```
POST /ask
```

**Request:**

```json
{
  "query": "How do I reset my password?"
}
```

---

### 🔹 Authentication

```
POST /signup
POST /login
POST /logout
```

---

## 📁 Project Structure

```
.
├── main.py
├── Dockerfile
├── requirements.txt
├── api/
├── rag/
├── config/
├── data/
├── faiss_index/
```

---

## ⚡ Setup (Local)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🚀 Deployment

* Platform: Hugging Face Spaces
* Type: Docker-based deployment
* Port: 7860

---

## 🔮 Future Improvements

* Add LLM for multi-document reasoning
* Improve semantic understanding
* Add React frontend UI
* Implement role-based authentication
* Add logging & monitoring

---

## 👨‍💻 Author

**Dinesh Kumar**

---

## 📄 License

This project is open-source and available under the MIT License.

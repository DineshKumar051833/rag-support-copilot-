import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# load dataset
with open("../data/docs.json") as f:
    data = json.load(f)

documents = []

for item in data:
    text = item["question"] + " " + item["answer"]
    documents.append(Document(page_content=text))

# load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# create FAISS vector DB
vector_db = FAISS.from_documents(documents, embeddings)

# save database
vector_db.save_local("../faiss_index")

print("Vector database created successfully!")

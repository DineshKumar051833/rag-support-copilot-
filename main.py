from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "RAG Support Copilot is running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://10.249.231.52:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

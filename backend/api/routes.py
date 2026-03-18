from fastapi import APIRouter
from pydantic import BaseModel
from rag.rag_pipeline import ask_question
from api.auth import signup_user, login_user
from fastapi import Request

router = APIRouter()


class AuthRequest(BaseModel):
    username: str
    password: str


# Request body model
class QueryRequest(BaseModel):
    query: str


# API endpoint
@router.post("/ask")
def ask(request: Request, body: QueryRequest):

    # Check session
    if "user" not in request.session:
        return {
            "error": "Unauthorized. Please login first."
        }

    query = body.query.strip()
    response = ask_question(query)
    return response


@router.post("/signup")
def signup(request: AuthRequest):
    success, message = signup_user(request.username, request.password)

    return {
        "success": success,
        "message": message
    }


@router.post("/login")
def login(request: Request, body: AuthRequest):
    success, message = login_user(body.username, body.password)

    if success:
        request.session["user"] = body.username  # store session

    return {
        "success": success,
        "message": message
    }


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

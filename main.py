from fastapi import FastAPI
from api.routes import router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",
)

app.include_router(router)

app.mount("/static", StaticFiles(directory="build/static"), name="static")


@app.get("/")
def serve():
    return FileResponse("build/index.html")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api import auth_api, game_api
from app.core.config import settings

app = FastAPI(title="ELLP - Ferramenta de Movimentação de Personagem")

# guarda o "state" do OAuth durante o redirecionamento ao Google
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    https_only=settings.ENVIRONMENT == "production",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_api.router)
app.include_router(game_api.router)


@app.get("/")
def root():
    return {"status": "ok"}
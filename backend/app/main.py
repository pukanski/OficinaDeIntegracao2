from fastapi import FastAPI

from app.api import auth_api

app = FastAPI(title="ELLP - Ferramenta de Movimentação de Personagem")

app.include_router(auth_api.router)


@app.get("/")
def root():
    return {"status": "ok"}
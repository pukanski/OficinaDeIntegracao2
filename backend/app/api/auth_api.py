from fastapi import APIRouter, Depends, HTTPException, Request, status
from authlib.integrations.starlette_client import OAuthError
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.oauth import oauth
from app.models.user_model import User
from app.schemas.user_schema import UsuarioCreate, UsuarioOut
from app.schemas.auth_schema import LoginRequest, Token
from app.services import auth_service

from urllib.parse import quote

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        usuario = auth_service.criar_usuario(db, dados)
    except ValueError as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro))
    return usuario

@router.post("/login", response_model=Token)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = auth_service.autenticar_usuario(db, dados.email, dados.senha)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )
    token = auth_service.gerar_token_para_usuario(usuario)
    return Token(access_token=token)

@router.post("/token", response_model=Token)
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Usado pelo botão Authorize do /docs. O campo 'username' recebe o e-mail."""
    usuario = auth_service.autenticar_usuario(db, form.username, form.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )
    return Token(access_token=auth_service.gerar_token_para_usuario(usuario))


@router.get("/me", response_model=UsuarioOut)
def me(usuario: User = Depends(get_current_user)):
    return usuario


def _erro_front(codigo: str) -> RedirectResponse:
    return RedirectResponse(f"{settings.FRONTEND_URL}/login.html?erro={quote(codigo)}")


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token_google = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return _erro_front("google")

    info = token_google.get("userinfo")
    if not info or not info.get("email") or not info.get("email_verified"):
        return _erro_front("google_email")

    usuario = auth_service.login_ou_criar_usuario_google(
        db,
        google_id=info["sub"],
        email=info["email"],
        nome=info.get("name") or info["email"],
    )
    jwt_app = auth_service.gerar_token_para_usuario(usuario)
    return RedirectResponse(f"{settings.FRONTEND_URL}/auth-callback.html#token={jwt_app}")
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UsuarioCreate
from app.core.security import hash_senha


def email_ja_cadastrado(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None


def validar_dados_cadastro(dados: UsuarioCreate) -> None:
    if len(dados.senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres")


def criar_usuario(db: Session, dados: UsuarioCreate) -> User:
    validar_dados_cadastro(dados)

    if email_ja_cadastrado(db, dados.email):
        raise ValueError("Email já cadastrado")

    usuario = User(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
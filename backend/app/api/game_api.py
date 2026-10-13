from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user_model import User
from app.schemas.game_schema import FaseOut, ProgressoCreate, ProgressoOut, StatsOut
from app.services import progresso_service
from app.services.progresso_service import FaseBloqueada, FaseNaoEncontrada

router = APIRouter(tags=["jogo"])


@router.get("/fases", response_model=list[FaseOut])
def listar_fases(usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return progresso_service.listar_fases_do_usuario(db, usuario.id)


@router.post("/progresso", response_model=ProgressoOut, status_code=status.HTTP_201_CREATED)
def salvar_progresso(
    dados: ProgressoCreate,
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return progresso_service.registrar_tentativa(db, usuario.id, dados)
    except FaseNaoEncontrada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fase não encontrada")
    except FaseBloqueada:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Fase ainda bloqueada")


@router.get("/stats", response_model=StatsOut)
def obter_stats(usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return progresso_service.calcular_stats(db, usuario.id)
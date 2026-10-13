from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.tentativa_model import Tentativa
from app.schemas.game_schema import (
    FaseOut,
    ProgressoCreate,
    ProgressoOut,
    StatsFase,
    StatsOut,
)
from app.services.fase_service import FASES, Fase, obter_fase, simular


class FaseNaoEncontrada(Exception):
    pass


class FaseBloqueada(Exception):
    pass


def _fases_concluidas(db: Session, usuario_id: int) -> set[int]:
    linhas = (
        db.query(Tentativa.fase_id)
        .filter(Tentativa.user_id == usuario_id, Tentativa.concluida.is_(True))
        .distinct()
        .all()
    )
    return {fase_id for (fase_id,) in linhas}


def _liberada(fase: Fase, concluidas: set[int]) -> bool:
    """A primeira fase é sempre liberada; as demais exigem a anterior concluída."""
    indice = FASES.index(fase)
    return indice == 0 or FASES[indice - 1].id in concluidas


def listar_fases_do_usuario(db: Session, usuario_id: int) -> list[FaseOut]:
    concluidas = _fases_concluidas(db, usuario_id)
    linhas = (
        db.query(Tentativa.fase_id, func.count(Tentativa.id))
        .filter(Tentativa.user_id == usuario_id)
        .group_by(Tentativa.fase_id)
        .all()
    )
    tentativas = {fase_id: qtd for fase_id, qtd in linhas}

    return [
        FaseOut(
            id=f.id,
            titulo=f.titulo,
            descricao=f.descricao,
            largura=f.largura,
            altura=f.altura,
            inicio=f.inicio,
            destino=f.destino,
            obstaculos=list(f.obstaculos),
            concluida=f.id in concluidas,
            liberada=_liberada(f, concluidas),
            tentativas=tentativas.get(f.id, 0),
        )
        for f in FASES
    ]


def registrar_tentativa(db: Session, usuario_id: int, dados: ProgressoCreate) -> ProgressoOut:
    fase = obter_fase(dados.fase_id)
    if fase is None:
        raise FaseNaoEncontrada()
    if not _liberada(fase, _fases_concluidas(db, usuario_id)):
        raise FaseBloqueada()

    # o servidor reproduz os movimentos: quem decide se a fase foi concluída é ele, não o cliente
    resultado = simular(fase, dados.movimentos)

    db.add(
        Tentativa(
            user_id=usuario_id,
            fase_id=fase.id,
            concluida=resultado.concluida,
            movimentos=resultado.movimentos_validos,
            tempo_segundos=dados.tempo_segundos,
        )
    )
    db.commit()

    total = (
        db.query(func.count(Tentativa.id))
        .filter(Tentativa.user_id == usuario_id, Tentativa.fase_id == fase.id)
        .scalar()
    )
    return ProgressoOut(
        fase_id=fase.id,
        concluida=resultado.concluida,
        posicao_final=resultado.posicao_final,
        movimentos_validos=resultado.movimentos_validos,
        tentativas_na_fase=total,
    )


def calcular_stats(db: Session, usuario_id: int) -> StatsOut:
    linhas = (
        db.query(
            Tentativa.fase_id,
            func.count(Tentativa.id),
            func.sum(case((Tentativa.concluida.is_(True), 1), else_=0)),
            func.sum(Tentativa.tempo_segundos),
        )
        .filter(Tentativa.user_id == usuario_id)
        .group_by(Tentativa.fase_id)
        .all()
    )
    por_id = {fase_id: (qtd, int(ok or 0), int(tempo or 0)) for fase_id, qtd, ok, tempo in linhas}

    por_fase = []
    for f in FASES:
        qtd, ok, tempo = por_id.get(f.id, (0, 0, 0))
        por_fase.append(
            StatsFase(fase_id=f.id, titulo=f.titulo, tentativas=qtd, concluida=ok > 0, tempo_segundos=tempo)
        )

    return StatsOut(
        fases_concluidas=sum(1 for s in por_fase if s.concluida),
        total_fases=len(FASES),
        total_tentativas=sum(s.tentativas for s in por_fase),
        tempo_total_segundos=sum(s.tempo_segundos for s in por_fase),
        por_fase=por_fase,
    )
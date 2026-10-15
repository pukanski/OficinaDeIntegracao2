from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Direcao = Literal["cima", "baixo", "esquerda", "direita"]


class Posicao(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int
    y: int


class FaseOut(BaseModel):
    id: int
    titulo: str
    descricao: str
    largura: int
    altura: int
    inicio: Posicao
    destino: Posicao
    obstaculos: list[Posicao]
    concluida: bool
    liberada: bool
    tentativas: int


class ProgressoCreate(BaseModel):
    fase_id: int
    movimentos: list[Direcao] = Field(min_length=1, max_length=1000)
    tempo_segundos: int = Field(ge=0, le=86400)


class ProgressoOut(BaseModel):
    fase_id: int
    concluida: bool
    posicao_final: Posicao
    movimentos_validos: int
    tentativas_na_fase: int


class StatsFase(BaseModel):
    fase_id: int
    titulo: str
    tentativas: int
    concluida: bool
    tempo_segundos: int


class StatsOut(BaseModel):
    fases_concluidas: int
    total_fases: int
    total_tentativas: int
    tempo_total_segundos: int
    por_fase: list[StatsFase]


class TentativaOut(BaseModel):
    id: int
    fase_id: int
    fase_titulo: str
    concluida: bool
    movimentos: int
    tempo_segundos: int
    criado_em: datetime | None

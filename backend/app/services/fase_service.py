"""Definição das fases e regras do jogo. Sem acesso a banco: lógica pura e testável."""
from dataclasses import dataclass

from app.schemas.game_schema import Direcao, Posicao


@dataclass(frozen=True)
class Fase:
    id: int
    titulo: str
    descricao: str
    largura: int
    altura: int
    inicio: Posicao
    destino: Posicao
    obstaculos: tuple[Posicao, ...]


def _p(x: int, y: int) -> Posicao:
    return Posicao(x=x, y=y)


# y cresce para baixo (y=0 é a linha de cima), igual ao grid do front-end.
FASES: tuple[Fase, ...] = (
    Fase(
        id=1,
        titulo="Primeiros passos",
        descricao="Leve o robô até a bandeira usando as setas.",
        largura=4, altura=4,
        inicio=_p(0, 0), destino=_p(3, 3),
        obstaculos=(),
    ),
    Fase(
        id=2,
        titulo="Desvie da parede",
        descricao="Há uma parede de pedras no caminho. Encontre a passagem.",
        largura=5, altura=5,
        inicio=_p(0, 0), destino=_p(4, 4),
        obstaculos=(_p(2, 0), _p(2, 1), _p(2, 2)),
    ),
    Fase(
        id=3,
        titulo="Labirinto",
        descricao="Planeje o caminho antes de se mover: há mais de um jeito de chegar.",
        largura=6, altura=6,
        inicio=_p(0, 0), destino=_p(5, 5),
        obstaculos=(_p(1, 0), _p(1, 1), _p(1, 2), _p(3, 1), _p(3, 2), _p(3, 3), _p(3, 4)),
    ),
)

DELTAS: dict[str, tuple[int, int]] = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
}


def obter_fase(fase_id: int) -> Fase | None:
    return next((f for f in FASES if f.id == fase_id), None)


def mover(fase: Fase, posicao: Posicao, direcao: Direcao) -> Posicao:
    """Retorna a nova posição, ou a mesma se o movimento for inválido (fora do grid ou obstáculo)."""
    dx, dy = DELTAS[direcao]
    x, y = posicao.x + dx, posicao.y + dy
    dentro = 0 <= x < fase.largura and 0 <= y < fase.altura
    if not dentro or _p(x, y) in fase.obstaculos:
        return posicao
    return _p(x, y)


def chegou_ao_destino(fase: Fase, posicao: Posicao) -> bool:
    return posicao == fase.destino


@dataclass(frozen=True)
class ResultadoSimulacao:
    posicao_final: Posicao
    concluida: bool
    movimentos_validos: int


def simular(fase: Fase, movimentos: list[Direcao]) -> ResultadoSimulacao:
    """Reproduz os movimentos a partir do início. Movimentos inválidos são ignorados.
    A fase é concluída assim que o destino é alcançado; o que sobrar da lista é descartado."""
    posicao = fase.inicio
    validos = 0
    for direcao in movimentos:
        nova = mover(fase, posicao, direcao)
        if nova == posicao:
            continue
        posicao = nova
        validos += 1
        if chegou_ao_destino(fase, posicao):
            return ResultadoSimulacao(posicao, True, validos)
    return ResultadoSimulacao(posicao, False, validos)
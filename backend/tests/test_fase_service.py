import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "chave-de-teste")

from collections import deque

from app.schemas.game_schema import Posicao
from app.services.fase_service import FASES, DELTAS, chegou_ao_destino, mover, obter_fase, simular


def p(x, y):
    return Posicao(x=x, y=y)


def tem_solucao(fase) -> bool:
    visitados, fila = {fase.inicio}, deque([fase.inicio])
    while fila:
        atual = fila.popleft()
        if atual == fase.destino:
            return True
        for direcao in DELTAS:
            nova = mover(fase, atual, direcao)
            if nova not in visitados:
                visitados.add(nova)
                fila.append(nova)
    return False


def test_toda_fase_tem_solucao():
    for fase in FASES:
        assert tem_solucao(fase), f"fase {fase.id} não tem solução"


def test_inicio_e_destino_nao_sao_obstaculos():
    for fase in FASES:
        assert fase.inicio not in fase.obstaculos
        assert fase.destino not in fase.obstaculos


def test_movimento_valido_atualiza_posicao():
    fase = obter_fase(1)
    assert mover(fase, p(0, 0), "direita") == p(1, 0)
    assert mover(fase, p(1, 1), "cima") == p(1, 0)


def test_movimento_para_fora_do_grid_e_bloqueado():  # CT12
    fase = obter_fase(1)
    assert mover(fase, p(0, 0), "esquerda") == p(0, 0)
    assert mover(fase, p(0, 0), "cima") == p(0, 0)
    assert mover(fase, p(3, 3), "direita") == p(3, 3)
    assert mover(fase, p(3, 3), "baixo") == p(3, 3)


def test_movimento_contra_obstaculo_e_bloqueado():  # CT12
    fase = obter_fase(2)  # obstáculo em (2, 0)
    assert mover(fase, p(1, 0), "direita") == p(1, 0)


def test_chegada_ao_destino_conclui_a_fase():  # CT13
    fase = obter_fase(1)
    resultado = simular(fase, ["direita"] * 3 + ["baixo"] * 3)
    assert resultado.concluida
    assert resultado.posicao_final == fase.destino
    assert chegou_ao_destino(fase, resultado.posicao_final)
    assert resultado.movimentos_validos == 6


def test_sem_chegar_ao_destino_nao_conclui():
    resultado = simular(obter_fase(1), ["direita", "baixo"])
    assert not resultado.concluida
    assert resultado.posicao_final == p(1, 1)


def test_movimentos_invalidos_sao_ignorados_e_nao_contam():
    resultado = simular(obter_fase(1), ["esquerda", "cima", "direita"])
    assert resultado.posicao_final == p(1, 0)
    assert resultado.movimentos_validos == 1


def test_movimentos_depois_da_chegada_sao_descartados():
    resultado = simular(obter_fase(1), ["direita"] * 3 + ["baixo"] * 3 + ["cima", "cima"])
    assert resultado.concluida
    assert resultado.posicao_final == obter_fase(1).destino
    assert resultado.movimentos_validos == 6
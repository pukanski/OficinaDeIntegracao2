import os

# Antes de importar o app: banco SQLite em memória, sem tocar no banco de desenvolvimento.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "chave-de-teste")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models import tentativa_model, user_model  # noqa: F401  (registram as tabelas)
from app.models.user_model import User
from app.schemas.game_schema import ProgressoCreate
from app.services import progresso_service
from app.services.progresso_service import FaseBloqueada, FaseNaoEncontrada

SOLUCAO_FASE_1 = ["direita"] * 3 + ["baixo"] * 3
# fase 2: desce até a linha 3, atravessa e desce até o destino
SOLUCAO_FASE_2 = ["baixo"] * 3 + ["direita"] * 4 + ["baixo"]


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    sessao = sessionmaker(bind=engine)()
    yield sessao
    sessao.close()


@pytest.fixture()
def usuario(db):
    u = User(nome="Ana", email="ana@email.com")
    db.add(u)
    db.commit()
    return u


def enviar(db, usuario, fase_id, movimentos, tempo=10):
    return progresso_service.registrar_tentativa(
        db, usuario.id, ProgressoCreate(fase_id=fase_id, movimentos=movimentos, tempo_segundos=tempo)
    )


def test_primeira_fase_liberada_e_demais_bloqueadas(db, usuario):
    fases = progresso_service.listar_fases_do_usuario(db, usuario.id)
    assert [f.liberada for f in fases] == [True, False, False]
    assert not any(f.concluida for f in fases)


def test_salva_tentativa_concluida(db, usuario):  # CT15
    r = enviar(db, usuario, 1, SOLUCAO_FASE_1)
    assert r.concluida
    assert r.tentativas_na_fase == 1


def test_progresso_persiste_e_libera_proxima_fase(db, usuario):  # CT14
    enviar(db, usuario, 1, SOLUCAO_FASE_1)
    fases = progresso_service.listar_fases_do_usuario(db, usuario.id)
    assert fases[0].concluida and fases[0].tentativas == 1
    assert fases[1].liberada and not fases[1].concluida
    assert not fases[2].liberada


def test_tentativa_incompleta_nao_conclui_nem_libera(db, usuario):
    r = enviar(db, usuario, 1, ["direita", "baixo"])
    assert not r.concluida
    fases = progresso_service.listar_fases_do_usuario(db, usuario.id)
    assert not fases[0].concluida
    assert fases[0].tentativas == 1
    assert not fases[1].liberada


def test_fase_bloqueada_e_recusada(db, usuario):
    with pytest.raises(FaseBloqueada):
        enviar(db, usuario, 2, SOLUCAO_FASE_2)


def test_fase_inexistente(db, usuario):
    with pytest.raises(FaseNaoEncontrada):
        enviar(db, usuario, 99, ["direita"])


def test_cliente_nao_consegue_forcar_conclusao(db, usuario):
    # ir apenas para a direita não chega ao destino, qualquer que seja o que o cliente alegue
    assert not enviar(db, usuario, 1, ["direita"] * 10).concluida


def test_stats_batem_com_o_progresso_salvo(db, usuario):  # CT18
    enviar(db, usuario, 1, ["direita"], tempo=5)      # falha
    enviar(db, usuario, 1, SOLUCAO_FASE_1, tempo=20)  # sucesso
    enviar(db, usuario, 2, SOLUCAO_FASE_2, tempo=30)  # sucesso

    s = progresso_service.calcular_stats(db, usuario.id)
    assert s.fases_concluidas == 2
    assert s.total_fases == 3
    assert s.total_tentativas == 3
    assert s.tempo_total_segundos == 55
    assert [(f.fase_id, f.tentativas, f.concluida, f.tempo_segundos) for f in s.por_fase] == [
        (1, 2, True, 25),
        (2, 1, True, 30),
        (3, 0, False, 0),
    ]


def test_stats_de_um_usuario_nao_incluem_o_de_outro(db, usuario):
    outro = User(nome="Bia", email="bia@email.com")
    db.add(outro)
    db.commit()
    enviar(db, outro, 1, SOLUCAO_FASE_1)

    s = progresso_service.calcular_stats(db, usuario.id)
    assert s.total_tentativas == 0
    assert s.fases_concluidas == 0


def test_historico_vem_do_mais_recente_para_o_mais_antigo(db, usuario):  # CT19
    enviar(db, usuario, 1, ["direita"], tempo=5)      # falha
    enviar(db, usuario, 1, SOLUCAO_FASE_1, tempo=20)  # sucesso

    h = progresso_service.listar_historico(db, usuario.id)
    assert [(t.fase_id, t.concluida, t.tempo_segundos) for t in h] == [(1, True, 20), (1, False, 5)]
    assert h[0].fase_titulo == "Primeiros passos"
    assert h[0].movimentos == 6
    assert h[1].movimentos == 1


def test_historico_respeita_o_limite(db, usuario):
    for _ in range(3):
        enviar(db, usuario, 1, ["direita"])

    assert len(progresso_service.listar_historico(db, usuario.id, limite=2)) == 2


def test_historico_de_um_usuario_nao_inclui_o_de_outro(db, usuario):
    outro = User(nome="Bia", email="bia@email.com")
    db.add(outro)
    db.commit()
    enviar(db, outro, 1, SOLUCAO_FASE_1)

    assert progresso_service.listar_historico(db, usuario.id) == []

"""
Testes de integração do endpoint de histórico.
Rodam contra o banco de teste, com rollback ao final de cada teste.
Casos de teste: CT19
"""
USUARIO = {"nome": "Ana Teste", "email": "ana.historico@example.com", "senha": "senha12345"}


def _autenticar(client) -> dict:
    client.post("/auth/register", json=USUARIO)
    resposta = client.post("/auth/login", json={"email": USUARIO["email"], "senha": USUARIO["senha"]})
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}


class TestHistorico:
    """RF11 — GET /historico"""

    def test_exige_autenticacao(self, client):
        assert client.get("/historico").status_code == 401

    def test_usuario_sem_tentativas_recebe_lista_vazia(self, client):
        response = client.get("/historico", headers=_autenticar(client))

        assert response.status_code == 200
        assert response.json() == []

    def test_lista_as_tentativas_da_mais_recente_para_a_mais_antiga(self, client):
        headers = _autenticar(client)
        client.post("/progresso", headers=headers,
                    json={"fase_id": 1, "movimentos": ["direita"], "tempo_segundos": 4})
        client.post("/progresso", headers=headers,
                    json={"fase_id": 1, "movimentos": ["direita"] * 3 + ["baixo"] * 3, "tempo_segundos": 12})

        response = client.get("/historico", headers=headers)

        assert response.status_code == 200
        corpo = response.json()
        assert [(t["concluida"], t["tempo_segundos"]) for t in corpo] == [(True, 12), (False, 4)]
        assert corpo[0]["fase_titulo"] == "Primeiros passos"
        assert corpo[0]["criado_em"] is not None

    def test_limite_invalido_retorna_422(self, client):
        response = client.get("/historico?limite=0", headers=_autenticar(client))

        assert response.status_code == 422

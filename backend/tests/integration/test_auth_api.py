"""
Testes de integração dos endpoints de autenticação.
Rodam contra o banco de teste, com rollback ao final de cada teste
Casos de teste: CT02, CT03, CT05, CT06
"""
from app.models.user_model import User

USUARIO = {"nome": "Ana Teste", "email": "ana@example.com", "senha": "senha12345"}

class TestCadastro:
    """RF01 — POST /auth/register"""

    def test_cadastro_valido_retorna_201(self, client):
        response = client.post("/auth/register", json=USUARIO)

        assert response.status_code == 201
        corpo = response.json()
        assert corpo["email"] == USUARIO["email"]
        assert corpo["nome"] == USUARIO["nome"]

    def test_resposta_nao_expoe_a_senha(self, client):
        corpo = client.post("/auth/register", json=USUARIO).json()

        assert "senha" not in corpo
        assert "senha_hash" not in corpo

    def test_senha_e_salva_com_hash_no_banco(self, client, db_session):
        client.post("/auth/register", json=USUARIO)

        usuario = db_session.query(User).filter(User.email == USUARIO["email"]).first()

        assert usuario is not None
        assert usuario.senha_hash != USUARIO["senha"]

    def test_email_duplicado_retorna_400(self, client):
        client.post("/auth/register", json=USUARIO)

        response = client.post("/auth/register", json=USUARIO)

        assert response.status_code == 400
        assert "cadastrado" in response.json()["detail"]

    def test_senha_curta_retorna_400(self, client):
        response = client.post("/auth/register", json={**USUARIO, "senha": "123"})

        assert response.status_code == 400

    def test_email_invalido_retorna_422(self, client):
        response = client.post("/auth/register", json={**USUARIO, "email": "invalido"})

        assert response.status_code == 422

class TestLogin:
    """RF02 — POST /auth/login"""

    def test_login_valido_retorna_token(self, client):
        client.post("/auth/register", json=USUARIO)

        response = client.post(
            "/auth/login",
            json={"email": USUARIO["email"], "senha": USUARIO["senha"]},
        )

        assert response.status_code == 200
        corpo = response.json()
        assert corpo["access_token"]
        assert corpo["token_type"] == "bearer"

    def test_senha_errada_retorna_401(self, client):
        client.post("/auth/register", json=USUARIO)

        response = client.post(
            "/auth/login",
            json={"email": USUARIO["email"], "senha": "senhaerrada"},
        )

        assert response.status_code == 401

    def test_email_inexistente_retorna_401(self, client):
        response = client.post(
            "/auth/login",
            json={"email": "naoexiste@example.com", "senha": "qualquercoisa"},
        )

        assert response.status_code == 401

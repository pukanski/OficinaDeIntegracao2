"""
Testes unitários do módulo de segurança (hash de senha e JWT).
Casos de teste: CT04
"""
from jose import jwt

from app.core.config import settings
from app.core.security import criar_access_token, hash_senha, verificar_senha

def test_hash_nao_guarda_senha_em_texto_puro():
    senha = "minhasenha123"
    assert hash_senha(senha) != senha

def test_senha_correta_autentica():
    senha_hash = hash_senha("minhasenha123")
    assert verificar_senha("minhasenha123", senha_hash) is True

def test_senha_incorreta_nao_autentica():
    senha_hash = hash_senha("minhasenha123")
    assert verificar_senha("senhaerrada", senha_hash) is False

def test_token_contem_os_dados_e_expiracao():
    token = criar_access_token({"sub": "42", "email": "ana@example.com"})

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload["sub"] == "42"
    assert payload["email"] == "ana@example.com"
    assert "exp" in payload

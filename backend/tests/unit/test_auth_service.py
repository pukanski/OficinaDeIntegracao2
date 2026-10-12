"""
Testes unitários das regras de validação do cadastro.
Casos de teste: CT01
"""
import pytest
from pydantic import ValidationError

from app.schemas.user_schema import UsuarioCreate
from app.services.auth_service import validar_dados_cadastro

def test_senha_curta_deve_falhar():
    dados = UsuarioCreate(nome="Ana", email="ana@example.com", senha="1234567")

    with pytest.raises(ValueError, match="pelo menos 8"):
        validar_dados_cadastro(dados)

def test_senha_com_tamanho_minimo_deve_passar():
    dados = UsuarioCreate(nome="Ana", email="ana@example.com", senha="12345678")

    validar_dados_cadastro(dados)

def test_email_em_formato_invalido_deve_falhar():
    with pytest.raises(ValidationError):
        UsuarioCreate(nome="Ana", email="email-invalido", senha="12345678")

"""
Configuração dos testes end-to-end (Selenium).
Pre requisitos:
- Google Chrome instalado
- API rodando em http://localhost:8000  (uvicorn app.main:app --reload)
Se a API não estiver no ar, os testes são pulados (skip), não falham.
"""
import httpx
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

API_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def api_disponivel():
    try:
        httpx.get(API_URL, timeout=2)
    except httpx.HTTPError:
        pytest.skip("API fora do ar em localhost:8000 (suba com uvicorn antes)")

@pytest.fixture()
def driver(api_disponivel):
    opcoes = Options()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1280,800")

    navegador = webdriver.Chrome(options=opcoes)
    navegador.implicitly_wait(5)
    yield navegador
    navegador.quit()

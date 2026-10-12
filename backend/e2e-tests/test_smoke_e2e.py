"""
Só confirma que o Selenium abre o navegador
e consegue carregar a aplicação. Os fluxos reais (login, movimentação do
personagem) entram aqui quando o front-end existir.
"""
from conftest import API_URL

def test_documentacao_da_api_abre_no_navegador(driver):
    driver.get(f"{API_URL}/docs")

    assert "ELLP" in driver.title

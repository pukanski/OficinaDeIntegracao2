"""confirma que a aplicação sobe e responde"""

def test_rota_raiz_responde_ok(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_check():
    response = client.get("/")

    assert response.status_code == 200, 'Exista o eroare la api'

    assert response.json() == {"status": "ok", "message": "Hello DevOps! Aplicatia functioneaza."}, "Aplicatia nu  functioneaza"
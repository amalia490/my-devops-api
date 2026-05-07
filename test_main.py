from fastapi.testclient import TestClient
from main import app

#client fals
client = TestClient(app)

def test_read_root():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {"status": "ok", "message": "Hello DevOps! Aplicatia functioneaza."}
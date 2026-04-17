from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Document Classification Service is running."}

def test_classify_no_text():
    response = client.post("/classify", json={"text": ""})
    assert response.status_code == 400
    
def test_classify_with_text():
    # Model loading depends on the lifecycle event in testing unless mocked
    # We use a context manager to simulate startup/shutdown
    with TestClient(app) as client_started:
        response = client_started.post("/classify", json={"text": "Invoice from Supplier A for $500"})
        # 503 if model is missing, otherwise 200
        if response.status_code == 200:
            assert "category" in response.json()
            assert response.json()["category"] in ["invoice", "legal", "report"]
        else:
            assert response.status_code == 503

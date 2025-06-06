from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_classes():
    res = client.get("/classes")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_book_class():
    res = client.post("/book", json={
        "class_id": 1,
        "client_name": "Test User",
        "client_email": "test@example.com"
    })
    assert res.status_code == 200
    assert res.json()["client_email"] == "test@example.com"

def test_overbook():
    # Book the class until full
    for _ in range(5):
        client.post("/book", json={
            "class_id": 2,
            "client_name": "User",
            "client_email": "u@example.com"
        })
    res = client.post("/book", json={
        "class_id": 2,
        "client_name": "User",
        "client_email": "u@example.com"
    })
    assert res.status_code == 400

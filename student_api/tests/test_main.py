from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_student():
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "grade": "9",
        "age": 14,
        "phone_number": "5551234567",
        "email": "alice@example.com",
        "address": "123 Road",
        "father_name": "Bob",
        "mother_name": "Carol"
    }
    response = client.post("/students", json=data)
    assert response.status_code == 201
    student = response.json()
    assert student["first_name"] == data["first_name"]
    student_id = student["id"]

    get_resp = client.get(f"/students/{student_id}")
    assert get_resp.status_code == 200
    assert get_resp.json() == student

    list_resp = client.get("/students")
    assert list_resp.status_code == 200
    assert any(s["id"] == student_id for s in list_resp.json())

from fastapi.testclient import TestClient
from requests.structures import CaseInsensitiveDict

ADMIN_HEADER = CaseInsensitiveDict(
    data={"Cookie":
          'Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hbmFnZXIiLCJuYW1lIjoiRnVsYW5vIGRlIFRhbCIsImpvYl9yb2xlIjoiRXN0YWdpYXJpbyIsImFjY2VzcyI6ImFkbWluIn0.vu3T9_4xAf2UWL8n4c-Wm3pM8JZTAmwdBubrFWgX7nM'})  # noqa 501

def test_get_student_by_registration_number(client: TestClient):
    registration_number = "0004"  # Replace with the desired registration number
    
    response = client.get(f"/user/{registration_number}", headers=ADMIN_HEADER)
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["matricula"] == registration_number
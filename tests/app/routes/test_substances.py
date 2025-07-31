import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_substances_available_route():
  """
  Testing '/substances' endpoint route
  """
  response = client.get("/substances")
  assert response.status_code == 200
import pytest


@pytest.mark.anyio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response JSON should have 'message' key"
    assert data["message"] == "Server is up and running", f"Unexpected message: {data['message']}"

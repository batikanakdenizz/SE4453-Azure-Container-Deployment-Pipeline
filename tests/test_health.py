def test_hello_returns_200(client):
    response = client.get("/hello")

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello from Azure App Service!"

from unittest.mock import MagicMock, patch


def _make_mock_conn(version: str = "PostgreSQL 16.0 on x86_64"):
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (version,)
    mock_cur.__enter__ = MagicMock(return_value=mock_cur)
    mock_cur.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.cursor.return_value = mock_cur
    return mock_conn


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_hello_returns_200_with_db(client):
    with patch("app.routes.health.get_connection", return_value=_make_mock_conn()):
        response = client.get("/hello")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["message"] == "Hello from Azure App Service!"
    assert data["database"]["connected"] is True
    assert "version" in data["database"]


def test_hello_returns_500_on_db_error(client):
    with patch("app.routes.health.get_connection", side_effect=Exception("connection refused")):
        response = client.get("/hello")

    assert response.status_code == 500
    data = response.get_json()
    assert data["status"] == "error"


def test_hello_returns_503_on_config_error(client):
    with patch("app.routes.health.get_connection", side_effect=EnvironmentError("KEY_VAULT_NAME not set")):
        response = client.get("/hello")

    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "error"

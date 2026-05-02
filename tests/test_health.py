from unittest.mock import MagicMock, patch


def test_hello_returns_200(client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = ("PostgreSQL 16.0 on x86_64",)
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    with patch("app.routes.health.get_connection", return_value=mock_conn):
        response = client.get("/hello")

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hello from Azure App Service!"
    assert "postgres_version" in data

import json
import urllib.request
from app.core.health import start_health_server


def test_health_check_server() -> None:
    # Usar un puerto dinámico de prueba
    port = 8888
    server = start_health_server(host="127.0.0.1", port=port)
    try:
        url = f"http://127.0.0.1:{port}/"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = json.loads(response.read().decode("utf-8"))
            assert data["status"] == "ok"
            assert data["service"] == "relu-backend"
    finally:
        server.shutdown()
        server.server_close()

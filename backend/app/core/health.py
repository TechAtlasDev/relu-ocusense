import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple

logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Handler simple de HTTP para responder a las verificaciones de salud de Cloud Run."""

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = json.dumps({"status": "ok", "service": "relu-backend"}).encode("utf-8")
        self.wfile.write(response)

    def log_message(self, format: str, *args: Tuple[object, ...]) -> None:
        # Silenciar los logs de acceso por cada probe de healthcheck de Cloud Run
        pass


def start_health_server(host: str = "0.0.0.0", port: int = 8080) -> HTTPServer:
    """Inicia un servidor HTTP en segundo plano en un daemon thread."""
    server = HTTPServer((host, port), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Servidor de Health Check iniciado en http://{host}:{port}/")
    return server

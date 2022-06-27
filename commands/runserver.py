import typer
import uvicorn
import os
from commands.base import ping
from commands.base import GunicornServer

typer_app = typer.Typer(help="Helper commands to run server in prod or dev")


@typer_app.command()
def dev(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True,
    log_level: str = "debug",
):
    """
    Start uvicorn for development with reload enabled. Also run basic checks.
    """
    if ping():
        uvicorn.run(
            "main:fastapi_application",
            host=host,
            port=port,
            log_level=log_level,
            reload=reload,
        )
    else:
        typer.echo("Redis is not reachable")


@typer_app.command()
def prod():
    """
    Start gunicorn with uvicorn workers. Also run basic checks
    """
    bind_ip = os.getenv("GUNICORN_BIND_IP", "0.0.0.0")
    bind_port = os.getenv("GUNICORN_BIND_PORT", "10080")
    gunicorn_workers = os.getenv("GUNICORN_WORKERS", "3")
    options = {
        "bind": f"{bind_ip}:{bind_port}",
        "workers": gunicorn_workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    GunicornServer("main:fastapi_application", options).run()

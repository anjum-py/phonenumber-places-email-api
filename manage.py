import typer
from commands.db import typer_app as commands_db
from commands.runserver import typer_app as app_server

typer_app = typer.Typer()
typer_app.add_typer(commands_db, name="db")
typer_app.add_typer(app_server, name="runserver")

if __name__ == "__main__":
    typer_app()

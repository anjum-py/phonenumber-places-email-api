import typer
from commands.base import ping, async_helper
from db.async_db import ManageCities, ManageCountries, ManageTimezones, build_db_info, WithinSetTime

typer_app = typer.Typer(help="Operations related to redis")

@typer_app.command()
def get_db_info():
    """
    Returns a dictionary with information about redis instance
    """
    if ping():
        typer.echo(f"\n{async_helper(build_db_info())}\n")
    else:
        typer.echo(f"\nRedis instance is not reachable\n")


@typer_app.command()
def populate_db(force: bool = typer.Option(False, help="Force update all indexes")):
    """
    Download and parse csv data and update redisearch indexes
    """

    indexes = [ManageCountries, ManageTimezones, ManageCities]
    if force:
        for index in indexes:
            async_helper(index().reset_elapsed_time())

    typer.echo(f"\nStarting db update. It takes a couple of minutes to download, parse, and update db")
    try:
        for index in indexes:
            typer.echo(f"\nDownloading {index.index.name}.csv")
            async_helper(index().download_file())
            typer.echo(f"Updating {index.index.name} database")
            async_helper(index().update_db())
            r = async_helper(index().get_index_info())
            typer.echo(f"Added {r} records to {index.index.name} index")
    except WithinSetTime as e:
            typer.echo(e.message)



import click
from .etl import (extract, transform_load)

@click.command()
def etl():
    """Run the full ETL pipeline"""
    click.echo('Downloading and extracting data')
    extract()
    click.echo("Transforming and loading data")
    transform_load()

@click.command()
def transload():
    """Transform and load data"""
    click.echo('Transloading data')
    transform_load()
    click.echo("Transloaded data")
    
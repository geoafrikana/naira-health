import click
from .download import (download_hf, extract_hf,
                       DATA_DIR)

@click.command()
@click.option('--geometries', '-g',
              type=click.Choice(['point', 'polygon'],
                                case_sensitive=False),
              default=['point', 'polygon'],
              multiple=True, help='point and/or polygon')
def download(geometries):
    """Download health facility data from Meta Humanitarian site"""
    for geometry in geometries:
        click.echo(f"Downloading hf {geometry}")
        download_hf(geometry)
        click.echo(f"Downloaded hf {geometry}")

@click.command()
@click.option('--geometries', '-g',
              type=click.Choice(['point', 'polygon'],
                                case_sensitive=False),
              default=['point', 'polygon'],
              multiple=True, help='point and/or polygon')
def extract(geometries):
    """Extract health facility to geojson"""
    for geometry in geometries:
        click.echo(f"Extracting hf {geometry}")
        extract_hf(DATA_DIR, geometry)
        click.echo(f"Extracted hf {geometry}")
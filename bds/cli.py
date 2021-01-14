import click
from app.core.cli import core_install
from bds.models import Municipality
from bds import bp_bds


@bp_bds.cli.command("install")
def install():

    if core_install():
        print("Installation complete!")

    else:
        print("Installation failed!")


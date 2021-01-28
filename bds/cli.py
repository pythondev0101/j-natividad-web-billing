from app import db
from app.core.cli import core_install
from app.auth.models import Role
from bds.models import Municipality
from bds import bp_bds


@bp_bds.cli.command("install")
def install():

    if core_install():
        print("Inserting system roles...")
        
        if not Role.query.count() == 1:
            print("Role already inserted!")

        role = Role()
        role.name = "Messengers"
        db.session.add(role)
        print("Messenger role inserted!")
        
        db.session.commit()
        
        print("Installation complete!")

    else:
        print("Installation failed!")


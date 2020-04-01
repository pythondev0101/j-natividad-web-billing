#TODO: create Base,Customer model
from app import db
from datetime import datetime


# MODEL.BASE
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    # TODO server_default=value
    active = db.Column(db.Boolean, nullable=False, default="1")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.active = 1


class CoreCustomer(Base):
    __abstract__ = True
    fname = db.Column(db.String(64), nullable=False, server_default="")
    lname = db.Column(db.String(64), nullable=False, server_default="")
    phone = db.Column(db.String(64), nullable=False, server_default="")
    email = db.Column(db.String(64), nullable=False, unique=True)
    zip = db.Column(db.Integer,nullable=False)
    street = db.Column(db.String(64), nullable=False,server_default="")


class CoreCity(Base):
    __abstract__ = True
    name = db.Column(db.String(64), nullable=False,server_default="")


class CoreProvince(Base):
    __abstract__ = True
    name = db.Column(db.String(64), nullable=False,server_default="")

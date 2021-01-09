from app import db
from app.admin.models import Admin
from app.core.models import Base
from datetime import datetime


class Subscriber(Base, Admin):
    __tablename__ = 'bds_subscribers'
    __amname__ = 'subscriber'
    __amdescription__ = 'Subscribers'
    __amicon__ = 'pe-7s-users'
    __list_view_url__ = 'bp_bds.subscribers'

    """ COLUMNS """
    fname = db.Column(db.String(64), nullable=True)
    mname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    contract_number = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(1000), nullable=True)
    phone_number = db.Column(db.String(64), nullable=True)
    longitude = db.Column(db.String(255),nullable=True)
    latitude = db.Column(db.String(255), nullable=True)
    deliveries = db.relationship('Delivery', cascade='all,delete', backref="subscriber")
    sub_area_id = db.Column(db.Integer, db.ForeignKey('bds_sub_area.id', ondelete="SET NULL"), nullable=True)
    sub_area = db.relationship('SubArea',backref="subscribers", uselist=False)

    @property
    def url(self):
        return "bp_bds.subscribers"


class Delivery(Base, Admin):
    __tablename__ = 'bds_delivery'
    __amname__ = 'delivery'
    __amdescription__ = 'Deliveries'
    __amicon__ = 'pe-7s-paper-plane'
    __amfunctions__ = []
    __list_view_url__ = 'bp_bds.deliveries'
    
    """ COLUMNS """
    subscriber_id = db.Column(db.Integer, db.ForeignKey('bds_subscribers.id', ondelete="SET NULL"), nullable=True)
    messenger_id = db.Column(db.Integer, db.ForeignKey('auth_user.id', ondelete="SET NULL"), nullable=True)
    delivery_date = db.Column(db.DateTime, default=datetime.utcnow,nullable=True)
    date_delivered = db.Column(db.DateTime, nullable=True)
    date_mobile_delivery = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(255), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    accuracy = db.Column(db.String(255), nullable=True)
    delivery_longitude = db.Column(db.String(255),nullable=True)
    delivery_latitude = db.Column(db.String(255), nullable=True)

    def __init__(self, subscriber_id, status):
        super(Delivery, self).__init__()
        self.subscriber_id = subscriber_id
        self.status = status


class Area(Base, Admin):
    __tablename__ = 'bds_area'
    __amname__ = 'area'
    __amdescription__ = 'Locations'
    __amicon__ = 'pe-7s-flag'
    __amfunctions__ = [
        {"Sub Areas": "bp_bds.sub_areas"},
        {"Areas": "bp_bds.areas"},
        {"Municipalities": "bp_bds.municipalities"},
        ]
    __list_view_url__ = 'bp_bds.areas'

    """ COLUMNS """
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.String(1000),nullable=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('bds_municipality.id'), nullable=True)
    municipality = db.relationship("Municipality", backref='areas')


class SubArea(Base, Admin):
    __tablename__ = 'bds_sub_area'
    __amname__ = 'sub_area'
    __amdescription__ = 'Sub Areas'
    __amicon__ = 'pe-7s-flag'
    __amfunctions__ = []
    #__list_view_url__ = 'bp_bds.areas'

    """ COLUMNS """
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.String(1000),nullable=True)
    area_id = db.Column(db.Integer, db.ForeignKey('bds_area.id', ondelete="SET NULL"), nullable=True)
    area = db.relationship('Area',backref="sub_areas")


class Messenger(db.Model, Admin):
    __abstract__ = True
    __tablename__ = 'auth_user'
    __amname__ = 'user'
    __amdescription__ = 'Messengers'
    __amicon__ = 'pe-7s-car'
    __amfunctions__ = []
    __list_view_url__ = 'bp_bds.messengers'


class Municipality(Base, Admin):
    __tablename__ = 'bds_municipality'
    __amname__ = 'municipality'
    __amdescription__ = 'Municipalities'
    __amicon__ = 'pe-7s-flag'
    __amfunctions__ = []

    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.String(1000),nullable=True)
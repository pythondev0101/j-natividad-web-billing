from flask_wtf import FlaskForm
from app.admin.forms import AdminTableForm, AdminEditForm, AdminInlineForm, AdminField
from wtforms.validators import DataRequired
from wtforms import StringField



class SubscriberForm(AdminTableForm):
    from .models import SubArea


    __table_columns__ = ['First name','Last name', 'Created at', 'updated at']
    __heading__ = "Subscribers"

    fname = AdminField(label="First name",validators=[DataRequired()])
    lname = AdminField(label="Last name",validators=[DataRequired()])
    email = AdminField(label="Email Address",required=False)
    address = AdminField(label="Address",required=False)
    longitude = AdminField(label="Longitude", required=False)
    latitude = AdminField(label="Latitude", required=False)
    contract_number = AdminField(label="Contract No.", validators=[DataRequired()])
    sub_area_id = AdminField(label="Sub Area", model=SubArea, required=False)

    @property
    def fields(self):
        return [
            [self.fname,self.lname, self.contract_number],[self.email,self.address],[self.longitude,self.latitude],[self.sub_area_id]
            ]


class DeliveriesInlineForm(AdminInlineForm):
    headers = ['Delivery id','Delivery Date','Date Delivered', 'Delivered By', 'Status', 'Actions']
    title = "Billings"
    html = 'bds/subscriber/deliveries_inline.html'


class SubscriberEditForm(AdminEditForm):
    from .models import SubArea

    __heading__ = 'Edit subscriber'

    fname = AdminField(label="First name",validators=[DataRequired()])
    lname = AdminField(label="Last name",validators=[DataRequired()])
    email = AdminField(label="Email Address",required=False)
    address = AdminField(label="Address",required=False)
    longitude = AdminField(label="Longitude", required=False)
    latitude = AdminField(label="Latitude", required=False)
    contract_number = AdminField(label="Contract No.", validators=[DataRequired()])
    sub_area_id = AdminField(label="Sub Area", required=False, model=SubArea)

    deliveries_inline = DeliveriesInlineForm()

    @property
    def fields(self):
        return [
            [self.fname,self.lname, self.contract_number],[self.email,self.address],[self.longitude,self.latitude],[self.sub_area_id]
            ]

    @property
    def inlines(self):
        return [self.deliveries_inline]


class MessengerForm(AdminTableForm):
    from .models import Area
    
    __table_columns__ = ['Username', 'First name', 'last name', 'email', 'created at', 'updated at']
    __heading__ = "Messengers"

    username = AdminField(label='Username', validators=[DataRequired()])
    email = AdminField(label='Email', type='email',required=False)
    fname = AdminField(label='First Name', validators=[DataRequired()])
    lname = AdminField(label='Last Name', validators=[DataRequired()])
    is_admin = AdminField(label='Is admin?',required=False, type='checkbox')

    @property
    def fields(self):
        return [[self.fname, self.lname],[self.username,self.email],[self.is_admin]]


class MessengerEditForm(AdminEditForm):
    from .models import Area

    __heading__ = 'Edit messenger'

    username = AdminField(label='Username', validators=[DataRequired()])
    email = AdminField(label='Email', type='email',required=False)
    fname = AdminField(label='First Name', validators=[DataRequired()])
    lname = AdminField(label='Last Name', validators=[DataRequired()])
    is_admin = AdminField(label='Is admin?',required=False, type='checkbox')

    @property
    def fields(self):
        return [[self.fname, self.lname],[self.username,self.email], [self.is_admin]]


class SubAreaForm(AdminTableForm):
    from .models import Area


    __table_columns__ = ['Name', 'description', 'Created at', 'updated at']
    __heading__ = "Sub areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    area_id = AdminField(label="Area", validators=[DataRequired()], model=Area)

    @property
    def fields(self):
        return [
            [self.name, self.description],
            [self.area_id]
        ]


class SubAreEditForm(AdminEditForm):
    from .models import Area


    __heading__ = "Sub areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    area_id = AdminField(label="Area", validators=[DataRequired()], model=Area)

    @property
    def fields(self):
        return [
            [self.name, self.description],
            [self.area_id]
        ]


class AreaForm(AdminTableForm):
    from bds.models import Municipality

    __table_columns__ = ['Name', 'description', 'Municipality', 'Created at', 'updated at']
    __heading__ = "Areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    municipality_id = AdminField(label="Municipality", required=False, model=Municipality)

    @property
    def fields(self):
        return [
            [self.name, self.description],
            [self.municipality_id]
        ]


class AreaEditForm(AdminEditForm):
    from bds.models import Municipality

    __heading__ = 'Edit Area'

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    municipality_id = AdminField(label="Municipality", required=False, model=Municipality)

    @property
    def fields(self):
        return []


class MunicipalityForm(AdminTableForm):
    __table_columns__ = ['Name', 'description', 'Created at', 'updated at']
    __heading__ = "Municipalities"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)

    @property
    def fields(self):
        return [
            [self.name, self.description]
        ]


class MunicipalityEditForm(AdminEditForm):
    __heading__ = 'Edit municipality'

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)

    @property
    def fields(self):
        return [
            [self.name, self.description]
        ]


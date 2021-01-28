from flask_wtf import FlaskForm
from app.admin.forms import AdminIndexForm,AdminEditForm, AdminInlineForm, AdminField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms import StringField



class SubscriberForm(AdminIndexForm):
    from .models import SubArea

    index_headers = ['First name','Last name', 'Created at', 'updated at']
    index_title = "Subscribers"

    fname = AdminField(label="First name",validators=[DataRequired()])
    lname = AdminField(label="Last name",validators=[DataRequired()])
    email = AdminField(label="Email Address",required=False)
    address = AdminField(label="Address",required=False)
    longitude = AdminField(label="Longitude", required=False)
    latitude = AdminField(label="Latitude", required=False)
    contract_number = AdminField(label="Contract No.", validators=[DataRequired()])
    sub_area_id = AdminField(label="Sub Area", model=SubArea, required=False)

    def create_fields(self):
        return [
            [self.fname,self.lname, self.contract_number],[self.email,self.address],[self.longitude,self.latitude],[self.sub_area_id]
            ]


class DeliveriesInlineForm(AdminInlineForm):
    headers = ['Delivery id','Delivery Date','Date Delivered', 'Delivered By', 'Status', 'Actions']
    title = "Billings"
    html = 'bds/subscriber/deliveries_inline.html'


class SubscriberEditForm(AdminEditForm):
    from .models import SubArea

    edit_title = 'Edit subscriber'

    fname = AdminField(label="First name",validators=[DataRequired()])
    lname = AdminField(label="Last name",validators=[DataRequired()])
    email = AdminField(label="Email Address",required=False)
    address = AdminField(label="Address",required=False)
    longitude = AdminField(label="Longitude", required=False)
    latitude = AdminField(label="Latitude", required=False)
    contract_number = AdminField(label="Contract No.", validators=[DataRequired()])
    sub_area_id = AdminField(label="Sub Area", required=False, model=SubArea)

    deliveries_inline = DeliveriesInlineForm()
    inlines = [deliveries_inline]

    def edit_fields(self):
        return [
            [self.fname,self.lname, self.contract_number],[self.email,self.address],[self.longitude,self.latitude],[self.sub_area_id]
            ]


class MessengerForm(AdminIndexForm):
    from .models import Area
    
    index_headers = ['Username', 'First name', 'last name', 'email', 'created at', 'updated at']
    index_title = "Messengers"

    username = AdminField(label='Username', validators=[DataRequired()])
    email = AdminField(label='Email', input_type='email',required=False)
    fname = AdminField(label='First Name', validators=[DataRequired()])
    lname = AdminField(label='Last Name', validators=[DataRequired()])
    is_admin = AdminField(label='Is admin?',required=False,input_type='checkbox')

    def create_fields(self):
        return [[self.fname, self.lname],[self.username,self.email],[self.is_admin]]


class MessengerEditForm(AdminEditForm):
    from .models import Area

    edit_title = 'Edit messenger'

    username = AdminField(label='Username', validators=[DataRequired()])
    email = AdminField(label='Email', input_type='email',required=False)
    fname = AdminField(label='First Name', validators=[DataRequired()])
    lname = AdminField(label='Last Name', validators=[DataRequired()])
    is_admin = AdminField(label='Is admin?',required=False,input_type='checkbox')

    def edit_fields(self):
        return [[self.fname, self.lname],[self.username,self.email], [self.is_admin]]


class AreaForm(AdminIndexForm):
    from bds.models import Municipality

    index_headers = ['Name', 'description', 'Created at', 'updated at']
    index_title = "Areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    municipality_id = AdminField(label="Municipality", required=False, model=Municipality)

    def create_fields(self):
        return [
            [self.name, self.description],
            [self.municipality_id]
        ]


class SubAreaForm(AdminIndexForm):
    from .models import Area

    index_headers = ['Name', 'description', 'Created at', 'updated at']
    index_title = "Sub areas"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    area_id = AdminField(label="Area", validators=[DataRequired()], model=Area)

    def create_fields(self):
        return [
            [self.name, self.description],
            [self.area_id]
        ]


class AreaEditForm(AdminEditForm):
    from bds.models import Municipality

    edit_title = 'Edit Area'

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)
    municipality_id = AdminField(label="Municipality", required=False, model=Municipality)

    def edit_fields(self):
        return [
            [self.name, self.description], [self.municipality_id]
        ]


class MunicipalityForm(AdminIndexForm):
    index_headers = ['Name', 'description', 'Created at', 'updated at']
    index_title = "Municipalities"

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)

    def create_fields(self):
        return [
            [self.name, self.description]
        ]


class MunicipalityEditForm(AdminEditForm):
    edit_title = 'Edit municipality'

    name = AdminField(label="Name",validators=[DataRequired()])
    description = AdminField(label="Description", required=False)

    def edit_fields(self):
        return [
            [self.name, self.description]
        ]


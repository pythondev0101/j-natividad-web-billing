from flask import Blueprint


bp_bds = Blueprint('bp_bds', __name__, template_folder='templates', static_folder='static',\
    static_url_path='/bds/static')

from . import api
from . import views
from . import uploads
from . import cli
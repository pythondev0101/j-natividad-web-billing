from flask_login import login_required
from app import CONTEXT
from app.admin.routes import admin_dashboard
from bds import bp_bds



@bp_bds.route('/')
@bp_bds.route('/dashboard')
@login_required
def dashboard():
    CONTEXT['active'] = 'delivery_map'

    return admin_dashboard('bds/bds_dashboard.html', title="Dashboard", module='bds')

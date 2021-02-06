from flask_login import login_required
from app.admin.templating import admin_render_template
from bds import bp_bds
from bds.models import DeliveryMap



@bp_bds.route('/')
@bp_bds.route('/delivery-map')
@login_required
def delivery_map():

    return admin_render_template(DeliveryMap, 'bds/bds_dashboard.html', 'bds', title="Dashboard")

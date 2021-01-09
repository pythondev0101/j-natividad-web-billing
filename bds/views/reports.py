from flask import render_template
from flask_login import login_required
from app import CONTEXT
from bds import bp_bds


@bp_bds.route('/reports')
@login_required
def reports():
    CONTEXT['module'] = 'bds'
    CONTEXT['active'] = 'report'
    return render_template('bds/bds_dashboard.html',context=CONTEXT, title="Reports")

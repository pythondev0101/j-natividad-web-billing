from flask import render_template
from flask_login import login_required
from app import CONTEXT
from bds import bp_bds



@bp_bds.route('/')
@bp_bds.route('/dashboard')
@login_required
def dashboard():
    CONTEXT['module'] = 'bds'
    CONTEXT['active'] = 'main_dashboard'
    return render_template('bds/bds_dashboard.html',context=CONTEXT, title="Dashboard",)

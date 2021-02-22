from datetime import datetime
from flask import redirect, url_for, request, flash, jsonify
from flask_login import  login_required, current_user
from app import db
from app.admin.templating import admin_table, admin_edit
from bds import bp_bds
from bds.models import Billing
from bds.forms import BillingForm, BillingEditForm
from bds.functions import generate_number



scripts = [
    {'bp_admin.static': 'js/admin_table.js'},
    {'bp_bds.static': 'js/billing.js'}
]


@bp_bds.route('/billings')
@login_required
def billings():
    fields = [
        Billing.id, Billing.active, Billing.number, Billing.name, Billing.description, Billing.date_from, 
        Billing.date_to, Billing.created_by, Billing.created_at]
    form = BillingForm()

    _billing_generated_number = ""

    query = db.session.query(Billing).order_by(Billing.id.desc()).first()

    if query:
        _billing_generated_number = generate_number("BILL", query.id)
    else:
        _billing_generated_number = "BILL00000001"

    form.number.auto_generated = _billing_generated_number

    return admin_table(Billing, fields=fields, form=form, create_url='bp_bds.create_billing',\
        edit_url="bp_bds.edit_billing", table_template="bds/bds_billing_table.html",\
            view_modal_template="bds/bds_billing_view_modal.html", scripts=scripts)


@bp_bds.route('/billings/create',methods=['POST'])
@login_required
def create_billing():
    form = BillingForm()
    
    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.billings'))
    
    try:
        new = Billing()
        new.active = 0
        new.number = form.number.data
        new.name = form.name.data
        new.description = form.description.data
        new.date_to = form.date_to.data
        new.date_from = form.date_from.data
        new.created_by = "{} {}".format(current_user.fname,current_user.lname)

        db.session.add(new)
        db.session.commit()
        flash('New billing added successfully!','success')

    except Exception as e:
        flash(str(e), 'error')

    return redirect(url_for('bp_bds.billings'))


@bp_bds.route('/billings/<int:oid>/edit',methods=['GET','POST'])
@login_required
def edit_billing(oid):
    ins = Billing.query.get_or_404(oid)
    form = BillingEditForm(obj=ins)

    if request.method == "GET":
        return admin_edit(Billing, form, 'bp_bds.edit_billing', oid, 'bp_bds.subscribers')

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.billings'))

    try:
        ins.name = form.name.data
        ins.description = form.description.data
        ins.date_to = form.date_to.data
        ins.date_from = form.date_from.data
        ins.updated_at = datetime.now()
        ins.updated_by = "{} {}".format(current_user.fname,current_user.lname)

        db.session.commit()
        flash('Billing update Successfully!','success')

    except Exception as e:
        flash(str(e),'error')

    return redirect(url_for('bp_bds.billings'))


@bp_bds.route('/billings/<int:billing_id>/set-active', methods=['POST'])
@login_required
def set_active(billing_id):
    status = request.json['status']

    response = jsonify({
        'result': True
    })

    try:
        billings = Billing.query.all()
        
        for billing in billings:
            if billing.id == billing_id:
                billing.active = status
            elif status == 1:
                billing.active = not status

        db.session.commit()

    except Exception:
        
        return jsonify({'result': False})

    return response
    

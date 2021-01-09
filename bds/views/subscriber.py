from datetime import datetime
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from app.admin.routes import admin_table, admin_edit
from bds import bp_bds
from bds.models import Subscriber
from bds.forms import SubscriberForm, SubscriberEditForm



@bp_bds.route('/subscribers')
@login_required
def subscribers():
    fields = [Subscriber.id, Subscriber.fname,Subscriber.lname,Subscriber.created_at, Subscriber.updated_at]
    form = SubscriberForm()
    return admin_table(Subscriber, fields=fields, form=form, template='bds/bds_table.html',create_url="bp_bds.create_subscriber",\
        edit_url="bp_bds.edit_subscriber", extra_modal="bds/bds_upload_subscribers_csv.html",\
            action="bds/bds_subscriber_action.html")


@bp_bds.route('/subscribers/create',methods=['POST'])
@login_required
def create_subscriber():
    form = SubscriberForm()
    
    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.subscribers'))
    
    try:
        new = Subscriber()
        new.fname = form.fname.data
        new.lname = form.lname.data
        new.email = form.email.data if form.email.data != '' else None
        new.address = form.address.data
        new.sub_area_id = form.sub_area_id.data if form.sub_area_id.data != '' else None
        new.longitude = form.longitude.data
        new.latitude = form.latitude.data
        new.contract_number = form.contract_number.data

        db.session.add(new)
        db.session.commit()
        flash('New subscriber added successfully!','success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('bp_bds.subscribers'))


@bp_bds.route('/subscribers/<int:oid>/edit',methods=['GET','POST'])
@login_required
def edit_subscriber(oid):
    ins = Subscriber.query.get_or_404(oid)
    form = SubscriberEditForm(obj=ins)
    if request.method == "GET":
        form.deliveries_inline.models = ins.deliveries

        return admin_edit(form,'bp_bds.edit_subscriber',oid, \
            model=Subscriber,template='bds/bds_edit.html')

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.subscribers'))

    try:
        ins.fname = form.fname.data
        ins.lname = form.lname.data
        ins.email = form.email.data if form.email.data != '' else None
        ins.address = form.address.data
        ins.sub_area_id = form.sub_area_id.data if form.sub_area_id.data != '' else None
        ins.longitude = form.longitude.data
        ins.latitude = form.latitude.data
        ins.contract_number = form.contract_number.data
        ins.updated_at = datetime.now()
        ins.updated_by = "{} {}".format(current_user.fname,current_user.lname)
        db.session.commit()
        flash('Subscriber update Successfully!','success')

    except Exception as e:
        flash(str(e),'error')
    return redirect(url_for('bp_bds.subscribers'))

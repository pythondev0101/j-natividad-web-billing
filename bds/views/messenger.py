from datetime import datetime
from flask import redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from app.admin.routes import admin_table, admin_edit
from app.auth.models import User
from bds import bp_bds
from bds.models import Messenger
from bds.forms import MessengerForm, MessengerEditForm



@bp_bds.route('/messengers',methods=['GET'])
@login_required
def messengers():
    form = MessengerForm()
    fields = [User.id, User.username, User.fname, User.lname, User.email, User.created_at, User.updated_at]
    models = [User]
    query = User.query.with_entities(*fields).filter_by(role_id=2).all()

    return admin_table(*models, fields=fields, list_view_url="bp_bds.messengers",\
        create_url='bp_bds.create_messenger', edit_url="bp_bds.edit_messenger", form=form,\
        kwargs={'module': 'bds','model_data':query}
        )


@bp_bds.route('/messengers/create', methods=['POST'])
@login_required
def create_messenger():
    form = MessengerForm()
    
    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.messengers'))

    try:
        new = User()
        new.fname = form.fname.data
        new.lname = form.lname.data
        new.email = form.email.data if form.email.data != '' else None
        new.username = form.username.data
        new.role_id = 2
        new.is_admin = 1 if form.is_admin.data == 'on' else 0
        new.set_password("password")
        new.is_superuser = 0
        db.session.add(new)
        db.session.commit()
        flash('New messenger added successfully!','success')
    except Exception as exc:
        flash(str(exc), 'error')

    return redirect(url_for('bp_bds.messengers'))


@bp_bds.route('/messengers/<int:oid>/edit',methods=['GET','POST'])
@login_required
def edit_messenger(oid):
    ins = User.query.get_or_404(oid)
    form = MessengerEditForm(obj=ins)

    if request.method == "GET":
        return admin_edit(form,'bp_bds.edit_messenger',oid, \
            model=Messenger,template='bds/bds_edit.html', kwargs={'module': 'bds'})

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.messengers'))

    try:
        ins.fname = form.fname.data
        ins.lname = form.lname.data
        ins.email = form.email.data if form.email.data != '' else None
        ins.username = form.username.data
        ins.is_admin = 1 if form.is_admin.data == 'on' else 0
        ins.updated_at = datetime.now()
        ins.updated_by = "{} {}".format(current_user.fname,current_user.lname)
        db.session.commit()

        flash('Messenger update Successfully!','success')
    except Exception as exc:
        flash(str(exc),'error')

    return redirect(url_for('bp_bds.messengers'))

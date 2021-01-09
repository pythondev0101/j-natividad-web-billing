from datetime import datetime
from flask import redirect, url_for, request, current_app, flash
from flask_login import current_user, login_required
from app import db
from app.admin.routes import admin_table, admin_edit
from bds import bp_bds
from bds.models import Municipality
from bds.forms import MunicipalityForm, MunicipalityEditForm


@bp_bds.route('/municipalities')
@login_required
def municipalities():
    fields = [Municipality.id, Municipality.name, Municipality.description, Municipality.created_at, Municipality.updated_at]
    form = MunicipalityForm()
    return admin_table(Municipality, fields=fields,form=form, template="bds/bds_table.html",\
        create_url='bp_bds.create_municipality', edit_url='bp_bds.edit_municipality')


@bp_bds.route('/municipalities/create', methods=['POST'])
@login_required
def create_municipality():
    form = MunicipalityForm()

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.municipalities'))

    try:
        new = Municipality()
        new.name = form.name.data
        new.description = form.description.data

        db.session.add(new)
        db.session.commit()

        flash('New municipality added successfully!')
    except Exception as exc:
        flash(str(exc), 'error')
    
    return redirect(url_for('bp_bds.municipalities'))


@bp_bds.route('/municipalities/<int:oid>/edit', methods=['GET', 'POST'])
@login_required
def edit_municipality(oid):
    ins = Municipality.query.get_or_404(oid)
    form = MunicipalityEditForm(obj=ins)

    if request.method == "GET":
        return admin_edit(form,'bp_bds.edit_municipality',oid, \
            model=Municipality,template='bds/bds_edit.html')

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.municipalities'))

    try:
        ins.name = form.name.data
        ins.description = form.description.data
        ins.updated_at = datetime.now()
        ins.updated_by = "{} {}".format(current_user.fname,current_user.lname)
        db.session.commit()

        flash('Municipality update Successfully!','success')
    except Exception as exc:
        flash(str(exc),'error')

    return redirect(url_for('bp_bds.municipalities'))

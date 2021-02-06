from datetime import datetime
from flask import redirect, url_for, request, flash, render_template
from flask_login import login_required
from app import db, CONTEXT
from app.admin.templating import admin_edit, admin_render_template
from app.admin.templating import admin_table
from bds import bp_bds
from bds.models import SubArea, Subscriber, Area
from bds.forms import SubAreEditForm, SubAreaForm



scripts = [
    {"bp_bds.static": "js/sub_area.js"}
]

modals = [
    "bds/sub_area/bds_add_subscriber_modal.html",
]


@bp_bds.route('/sub-areas')
@login_required
def sub_areas():
    fields = [SubArea.id,SubArea.name, SubArea.description, SubArea.created_at, SubArea.updated_at]
    form = SubAreaForm()

    return admin_table(SubArea, fields=fields,form=form, create_modal=False, create_button=True,\
        edit_url="bp_bds.edit_sub_area", create_url="bp_bds.create_sub_area")


@bp_bds.route('/sub-areas/create', methods=['GET','POST'])
@login_required
def create_sub_area():
    form = SubAreaForm()

    if request.method == "GET":
        _subscribers = Subscriber.query.all()
        _areas = Area.query.all()

        data = {
            'subscribers': _subscribers,
            'areas': _areas
        }

        return admin_render_template(SubArea, "bds/sub_area/bds_create_sub_area.html", 'bds', form=form,\
            data=data, modals=modals, scripts=scripts, title="Create sub area")

    try:
        new = SubArea()
        new.name = form.name.data
        new.description = form.description.data
        new.area_id = form.area_id.data if form.area_id.data != '' else None
        
        subscribers_line = request.form.getlist('subscribers[]')
        if subscribers_line:
            for sub_id in subscribers_line:
                subscriber = Subscriber.query.get_or_404(int(sub_id))
                new.subscribers.append(subscriber)

        db.session.add(new)
        db.session.commit()
        flash("New sub area added successfully!", 'success')
    except Exception as e:
        flash(str(e), 'error')

    return redirect(url_for('bp_bds.sub_areas'))


@bp_bds.route('/sub-areas/<int:oid>/edit', methods=['GET','POST'])
@login_required
def edit_sub_area(oid):
    ins = SubArea.query.get_or_404(oid)
    form = SubAreEditForm(obj=ins)

    if request.method == 'GET':
        _areas = Area.query.all()
        
        query = db.session.query(Subscriber.id).filter_by(sub_area_id=oid)
        _subscribers = db.session.query(Subscriber).filter(~Subscriber.id.in_(query)).all()
        
        data = {
            'subscribers': _subscribers,
            'areas': _areas,
            'ins_subscribers': ins.subscribers,
        }

        return admin_render_template(SubArea, 'bds/sub_area/bds_edit_sub_area.html', 'bds', oid=oid, \
            data=data, modals=modals, scripts=scripts, form=form,title="Edit sub area")

    try:
        ins.name = request.form.get('name')
        ins.description = request.form.get('description')
        ins.area_id = request.form.get('area_id') if not request.form.get('area_id') == '' else None
        
        subscribers_line = request.form.getlist('subscribers[]')
        ins.subscribers = []

        if subscribers_line:
            for sub_id in subscribers_line:
                subscriber = Subscriber.query.get_or_404(int(sub_id))
                ins.subscribers.append(subscriber)

        db.session.commit()
        flash("Sub area updated successfully!", 'success')
    except Exception as exc:
        flash(str(exc), 'error')
    
    return redirect(url_for('bp_bds.sub_areas'))

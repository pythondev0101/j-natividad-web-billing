from datetime import datetime
from flask import redirect, url_for, request, flash, render_template
from flask_login import login_required
from app import db, CONTEXT
from app.admin.routes import admin_table
from bds import bp_bds
from bds.models import SubArea, Subscriber, Area
from bds.forms import SubAreaForm


@bp_bds.route('/sub-areas')
@login_required
def sub_areas():
    fields = [SubArea.id,SubArea.name, SubArea.description, SubArea.created_at, SubArea.updated_at]
    form = SubAreaForm()

    return admin_table(SubArea, fields=fields,form=form, create_modal=False, create_button=True,\
        edit_url="bp_bds.edit_sub_area", create_url="bp_bds.create_sub_area", template='bds/bds_table.html')


@bp_bds.route('/sub-areas/create', methods=['GET','POST'])
@login_required
def create_sub_area():

    if request.method == "GET":

        _subscribers = Subscriber.query.all()
        _areas = Area.query.all()
        CONTEXT['module'] = 'bds'
        CONTEXT['model'] = 'sub_area'

        return render_template("bds/bds_create_sub_area.html",context=CONTEXT,\
            subscribers=_subscribers, areas=_areas, title="Create sub area")

    try:
        new = SubArea()
        new.name = request.form.get('name')
        new.description = request.form.get('description')
        new.area_id = request.form.get('area_id') if not request.form.get('area_id') == '' else None
        
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

    if request.method == 'GET':
        _areas = Area.query.all()
        
        query = db.session.query(Subscriber.id).filter_by(sub_area_id=oid)
        _subscribers = db.session.query(Subscriber).filter(~Subscriber.id.in_(query)).all()
        
        CONTEXT['module'] = 'bds'
        CONTEXT['model'] = 'sub_area'

        return render_template('bds/bds_edit_sub_area.html', context=CONTEXT,\
            oid=oid, subscribers=_subscribers,ins=ins,areas=_areas, title="Edit sub area")

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

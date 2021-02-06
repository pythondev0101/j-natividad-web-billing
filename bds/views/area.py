from flask import redirect, url_for, request, flash, render_template
from flask_login import login_required
from app import db, CONTEXT
from app.admin.templating import admin_render_template
from app.admin.templating import admin_table
from app.auth.models import User
from bds import bp_bds
from bds.models import Area, Municipality
from bds.forms import AreaEditForm, AreaForm



scripts = [
    {'bp_bds.static': 'js/area.js'}
]

modals = [
    "bds/area/bds_add_messenger_modal.html"
]


@bp_bds.route('/areas')
@login_required
def areas():
    models = [Area, Municipality]
    fields = [Area.id,Area.name, Area.description, Municipality.name, Area.created_at, Area.updated_at]
    form = AreaForm()

    return admin_table(*models, fields=fields,form=form, create_url='bp_bds.create_area',\
        create_button=True, edit_url="bp_bds.edit_area", create_modal=False)


@bp_bds.route('/areas/create', methods=["GET","POST"])
@login_required
def create_area():

    if request.method == "GET":
        _messengers = User.query.filter_by(role_id=2).all()
        _municipalities = Municipality.query.all()

        data = {
            'messengers': _messengers,
            'municipalities': _municipalities
        }

        return admin_render_template(Area, "bds/area/bds_create_area.html", 'bds', title="Create area",\
            data=data, modals=modals, scripts=scripts)

    try:
        new = Area()
        new.name = request.form.get('name', '')
        new.description = request.form.get('description', '')
        new.municipality_id = request.form.get('municipality_id') if request.form.get('municipality_id') != '' else None

        messengers_line = request.form.getlist('messengers[]')
        if messengers_line:
            for mes_id in messengers_line:
                messenger = User.query.get_or_404(int(mes_id))
                new.messengers.append(messenger)

        db.session.add(new)
        db.session.commit()
        
        flash('New Area added successfully!','success')
    except Exception as exc:
        flash(str(exc), 'error')

    return redirect(url_for('bp_bds.areas'))


@bp_bds.route('/areas/<int:oid>/edit', methods=['GET','POST'])
@login_required
def edit_area(oid):
    from app.auth.models import messenger_areas

    ins = Area.query.get_or_404(oid)
    form = AreaEditForm(obj=ins)
    if request.method == 'GET':
        
        query = db.session.query(User.id).join(messenger_areas).filter_by(area_id=oid)
        _messengers = db.session.query(User).filter(~User.id.in_(query)).filter_by(role_id=2).all()
        _municipalities = Municipality.query.all()

        data = {
            'messengers': _messengers,
            'municipalities': _municipalities
        }

        return admin_render_template(Area, 'bds/area/bds_edit_area.html', 'bds', oid=oid, ins=ins,form=form,\
            title="Edit area", data=data, scripts=scripts, modals=modals)
        
    try:
        ins.name = request.form.get('name', '')
        ins.description = request.form.get('description', '')
        ins.municipality_id = request.form.get('municipality_id') if request.form.get('municipality_id') != '' else None
        messengers_line = request.form.getlist('messengers[]')
        ins.messengers = []
        
        if messengers_line:
            for mes_id in messengers_line:
                messenger = User.query.get_or_404(int(mes_id))
                ins.messengers.append(messenger)

        db.session.commit()
        flash('Area updated Successfully!','success')
    except Exception as e:
        flash(str(e),'error')
    
    return redirect(url_for('bp_bds.areas'))

from bds.views.billing import billings
from flask import (json, url_for, request,jsonify, abort)
from flask_login import login_required
from flask_cors import cross_origin
from app import db, csrf
from app.admin.templating import admin_render_template
from bds import bp_bds
from bds.models import Billing, Delivery, SubArea, Municipality, Subscriber, Area



scripts = [
    {'bp_bds.static': 'js/delivery.js'},
    {'bp_bds.static': 'js/delivery_mdl_billing.js'}
]

modals = [
    'bds/delivery/bds_details_modal.html',
    'bds/delivery/bds_search_billing_modal.html'
]


@bp_bds.route('/deliveries',methods=['GET'])
@login_required
def deliveries():
    
    return admin_render_template(Delivery, 'bds/delivery/bds_delivery.html', 'bds', title="Delivery",\
        modals=modals, scripts=scripts)


@bp_bds.route('/api/deliveries/<string:contract_number>', methods=['GET'])
@cross_origin()
def get_delivery(contract_number):

    _sub_area_name = request.args['sub_area_name']
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

    delivery = Delivery.query.filter_by(active=1).join(Subscriber)\
        .filter_by(contract_number=contract_number,sub_area_id=sub_area.id).first()

    if delivery is None:
        return jsonify({
            'id': False
        })

    accuracy = 0
    if delivery.accuracy:
        accuracy = round(float(delivery.accuracy), 2)

    # WE SERIALIZE AND RETURN LIST INSTEAD OF MODELS

    return jsonify({
        'id': delivery.id,
        'subscriber_id': delivery.subscriber.id,
        'subscriber_fname': delivery.subscriber.fname,
        'subscriber_lname': delivery.subscriber.lname,
        'subscriber_address': delivery.subscriber.address,
        'delivery_date': delivery.delivery_date,
        'status': delivery.status,
        'longitude': delivery.delivery_longitude,
        'latitude': delivery.delivery_latitude,
        'accuracy': accuracy,
        'date_mobile_delivery': delivery.date_mobile_delivery,
        'image_path': url_for('bp_bds.static', filename=delivery.image_path),
        'messenger_fname': delivery.messenger.fname,
        'messenger_lname': delivery.messenger.lname
    })


@bp_bds.route('/api/delivery/<int:delivery_id>/confirm', methods=['POST'])
@cross_origin()
def confirm_delivery_id(delivery_id):

    delivery = Delivery.query.get_or_404(delivery_id)

    if delivery is None:
        abort(404)


    delivery.status = "DELIVERED"
    db.session.commit()

    return jsonify({
        'result':True, 
        'delivery': {'id': delivery.id,}
        })


@bp_bds.route('/api/subscriber/delivery/reset', methods=["POST"])
@cross_origin()
def reset():
    _subscriber_contract_no = request.json['subscriber_contract_no']
    _sub_area_name = request.json['sub_area_name']
    
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

    delivery = Delivery.query.filter_by(active=1).join(Subscriber)\
        .filter_by(contract_number=_subscriber_contract_no,sub_area_id=sub_area.id).first()

    if delivery is None:
        return jsonify({'result':False})

    delivery.active = 0
    db.session.commit()
    
    return jsonify({'result':True})


@bp_bds.route('/api/subscribers/<int:subscriber_id>/deliveries/deliver', methods=['POST'])
@cross_origin()
def deliver(subscriber_id):
    billing_id = request.json['billing_id']
    
    delivery = Delivery.query.filter_by(
        subscriber_id=subscriber_id, billing_id=billing_id, active=1
        ).first()

    if not delivery:
        new = Delivery(subscriber_id, "IN-PROGRESS")
        new.billing_id = billing_id

        db.session.add(new)
        db.session.commit()

    response = jsonify({'result':True})

    return response


@bp_bds.route('/api/deliveries/reset-all', methods=['POST'])
@cross_origin()
def reset_all():
    _sub_area_name = request.json['sub_area_name']
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

    if sub_area is None:
        abort(404)
    
    for subscriber in sub_area.subscribers:
        delivery = Delivery.query.filter_by(subscriber_id=subscriber.id,active=1).first()

        if delivery:
            delivery.active = 0
            db.session.commit()
    
    return jsonify({'result':True})


@bp_bds.route('/api/deliveries/deliver-all', methods=['POST'])
@cross_origin()
def deliver_all():
    billing_id = request.json['billing_id']
    _sub_area_name = request.json['sub_area_name']
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

    if not sub_area:
        abort(404)

    for subscriber in sub_area.subscribers:
        delivery = Delivery.query.filter_by(
            subscriber_id=subscriber.id, billing_id=billing_id, active=1
            ).first()
        
        if not delivery:
            new = Delivery(subscriber.id,"IN-PROGRESS")
            new.billing_id = billing_id

            db.session.add(new)
            db.session.commit()

    response = jsonify({'result': True})

    return response


@bp_bds.route('/api/get-municipality-areas', methods=["GET"])
@cross_origin()
def get_municipality_areas():

    _municipality_name = request.args.get('municipality_name')
    municipality = Municipality.query.filter_by(name=_municipality_name).first()

    if municipality is None:
        return jsonify({'result': False})

    data = []
    for area in municipality.areas:
        data.append({
            'id': area.id,
            'name': area.name,
            'description': area.description
        })

    return jsonify({'result': data})


@bp_bds.route('/api/get-area-sub-areas', methods=["GET"])
@cross_origin()
def get_area_sub_areas():

    _area_name = request.args.get('area_name')
    area = Area.query.filter_by(name=_area_name).first()

    if area is None:
        return jsonify(({'result': False}))
    
    data = []

    for sub_area in area.sub_areas:
        data.append({
            'id': sub_area.id,
            'name': sub_area.name,
            'description': sub_area.description
        })

    return jsonify({'result': data})


@bp_bds.route('/api/municipalities', methods=["GET"])
@cross_origin()
def get_municipalities():
    municipalities = Municipality.query.all()

    _data = []

    for municipality in municipalities:

        _data.append({
            'id': municipality.id,
            'name': municipality.name,
            'description': municipality.description
        })

    response = jsonify(_data)

    return response, 200


@bp_bds.route('/api/dtbl/billings', methods=['GET'])
@cross_origin()
def get_dtbl_billings():

    billings = Billing.query.all()

    _data = []

    for billing in billings:
        _data.append([
            billing.id,
            billing.number,
            billing.name,
            billing.date_from,
            billing.date_to,
        ])

    response = {
        'data': _data
        }

    print(response)

    return jsonify(response)

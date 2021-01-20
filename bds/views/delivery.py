from flask import (
    render_template, flash,
    redirect, url_for, request,
    jsonify, session, abort)
from flask_login import login_required
from sqlalchemy import or_
from app import db, CONTEXT, csrf
from bds import bp_bds
from bds.models import Delivery, SubArea, Municipality, Subscriber, Area



@bp_bds.route('/deliveries',methods=['GET'])
@login_required
def deliveries():

    _sub_areas = SubArea.query.all()
    _municipalities = Municipality.query.all()

    CONTEXT['active'] = 'delivery'
    CONTEXT['model'] = 'delivery'
    CONTEXT['module'] = 'bds'

    return render_template('bds/bds_delivery.html',context=CONTEXT,title="Delivery",\
        subAreas=_sub_areas, municipalities=_municipalities)


@bp_bds.route('/api/get-sub-area-subscribers')
@csrf.exempt
def get_sub_area_subscribers():

    _sub_area_name = request.args.get('sub_area_name')
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

    draw = request.args.get('draw')
    start, length = request.args.get('start'), request.args.get('length')
    search_value = "%" + request.args.get("search[value]") + "%"
     
    if not sub_area:
        return jsonify({'data':[],'recordsTotal':0,'recordsFiltered':0,'draw':draw})


    if search_value == "":
        query = Subscriber.query.filter_by(sub_area_id=sub_area.id)
    else:
        query = Subscriber.query.filter_by(sub_area_id=sub_area.id)\
            .filter(or_(Subscriber.lname.like(search_value),Subscriber.contract_number.like(search_value)))

    subscribers = query.limit(length).offset(start).all()
    total_records = query.count()

    data = []

    for subscriber in subscribers:

        delivery = Delivery.query.filter_by(subscriber_id=subscriber.id,active=1).first()

        _status = ""

        if delivery:
            _status = delivery.status
        else:
            _status = "NOT YET DELIVERED"

        data.append([
            subscriber.contract_number,
            subscriber.fname + " " + subscriber.lname,
            subscriber.address,
            _status,
            ""
        ])
    
    result = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    session['current_sub_area'] = sub_area.name

    return jsonify(result)


@bp_bds.route('/api/deliveries/<string:contract_number>', methods=['GET'])
@csrf.exempt
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
@csrf.exempt
def confirm_delivery_id(delivery_id):

    delivery = Delivery.query.get_or_404(delivery_id)

    if delivery is None:
        abort(404)


    delivery.status = "DELIVERED"
    db.session.commit()

    return jsonify({
        'result':True, 
        'delivery': {
            'id': delivery.id,
        }
        })


@bp_bds.route('/api/subscriber/delivery/reset', methods=["POST"])
@csrf.exempt
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


@bp_bds.route('/api/subscriber/delivery/deliver', methods=['POST'])
@csrf.exempt
def deliver():
    _subscriber_contract_no = request.json['subscriber_contract_no']
    _sub_area_name = request.json['sub_area_name']
    print(_sub_area_name)
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()
    
    delivery = Delivery.query.filter_by(active=1).join(Subscriber)\
        .filter_by(contract_number=_subscriber_contract_no, sub_area_id=sub_area.id).first()

    if delivery:
        pass
    else:
        subscriber = Subscriber.query.filter_by(contract_number=_subscriber_contract_no).first()
        new = Delivery(subscriber.id, "IN-PROGRESS")
        db.session.add(new)
        db.session.commit()

    return jsonify({'result':True})


@bp_bds.route('/api/deliveries/reset-all', methods=['POST'])
@csrf.exempt
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
@csrf.exempt
def deliver_all():

    _sub_area_name = request.json['sub_area_name']
    print(_sub_area_name)
    sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

    if sub_area:
        print("!!!!")
        for subscriber in sub_area.subscribers:

            delivery = Delivery.query.filter_by(subscriber_id=subscriber.id,active=1).first()
            if delivery:
                pass
            #     if deliver.status == "DELIVERED":
            #         pass
            #     elif deliver.status == "IN-PROGRESS":
            #         pass
            #     elif deliver.status == "PENDING":
            #         pass

            else:
                new = Delivery(subscriber.id,"IN-PROGRESS")
                db.session.add(new)
                db.session.commit()

    return jsonify({'result': True})


@bp_bds.route('/api/get-municipality-areas', methods=["GET"])
@csrf.exempt
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

    session['current_municipality'] = municipality.name

    if session.get('current_area', False):
        session.pop('current_area')

    if session.get('current_sub_area', False):
        session.pop('current_sub_area')

    return jsonify({'result': data})


@bp_bds.route('/api/get-area-sub-areas', methods=["GET"])
@csrf.exempt
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
    
    session['current_area'] = area.name

    if session.get('current_sub_area', False):
        session.pop('current_sub_area')

    return jsonify({'result': data})
import os
import json
from datetime import datetime
from math import pi, cos, sqrt
from werkzeug.utils import secure_filename
from flask import (jsonify, request, current_app)
# from flask_cors import cross_origin
from app import db, csrf
from app.auth.models import User
from bds import bp_bds
from bds.models import Delivery, Subscriber, Area, SubArea


@bp_bds.route('/api/confirm-deliver', methods=['POST'])
@csrf.exempt
def confirm_deliver():

    # FETCH DATA
    data = json.loads(request.form['data'])
    print(data)
    longitude = data['longitude']
    latitude = data['latitude']
    accuracy = data['accuracy']
    messenger_id = data['messenger_id']
    subscriber_id = data['subscriber_id']
    date_mobile_delivery = data['date_mobile_delivery']
    delivery = Delivery.query.filter_by(subscriber_id=subscriber_id,status="IN-PROGRESS",active=1).first()
    
    print(date_mobile_delivery)

    if delivery is None:
        return jsonify({'result': True})

    if _isCoordsNear(longitude, latitude, delivery.subscriber, .1):
        delivery.status = "DELIVERED"
        print("DELIVERED", delivery.id)
    else:
        delivery.status = "PENDING"
        print("PENDING", delivery.id)

    date = datetime.strptime(date_mobile_delivery, '%m/%d/%Y, %I:%M:%S %p')

    img_file = request.files['file']
    
    if img_file is None:
        return jsonify({'result': False})

    filename = secure_filename(img_file.filename)

    _img_path = os.path.join(current_app.config['UPLOAD_IMAGES_FOLDER'], filename)
    
    img_file.save(_img_path)
    print("IMAGE SAVED", subscriber_id)
    delivery.image_path = "img/uploads/" + filename
            
    delivery.messenger_id = messenger_id
    delivery.delivery_longitude = longitude
    delivery.delivery_latitude = latitude
    delivery.accuracy = accuracy
    delivery.date_mobile_delivery = date
    delivery.date_delivered = datetime.now()
    db.session.commit()
    print("Database updated", delivery.id)

    return jsonify({
        'result':True, 
        'delivery': {
            'id': delivery.id,
            'status': delivery.status
            }
        })


@bp_bds.route('/api/deliveries', methods=['GET'])
@csrf.exempt
def get_deliveries():
    from app.auth.models import messenger_areas

    _query = request.args.get('query')
    deliveries: Delivery

    if _query == 'by_messenger':
        _messenger_id = request.args.get('messenger_id')
        messenger = User.query.get_or_404(_messenger_id)
        query = db.session.query(Area.id).join(messenger_areas).filter_by(messenger_id=messenger.id)
        deliveries = db.session.query(Delivery).filter_by(active=1).join(Subscriber).join(SubArea).filter(SubArea.id.in_(query)).all()
    else:
        deliveries = Delivery.query.filter_by(active=1).all()

    print(_query)
    print(_messenger_id)
    print(db.session.query(Delivery).filter_by(active=1).join(Subscriber).join(SubArea).filter(SubArea.id.in_(query)))
    print(deliveries)
    # SERIALIZE MODELS
    _list = []
    for delivery in deliveries:
        _list.append({
            'id': delivery.id,
            'subscriber_id': delivery.subscriber.id,
            'subscriber_fname': delivery.subscriber.fname,
            'subscriber_lname': delivery.subscriber.lname,
            'subscriber_address': delivery.subscriber.address,
            'subscriber_email': delivery.subscriber.email,
            'delivery_date': delivery.delivery_date,
            'status': delivery.status,
            'longitude': delivery.subscriber.longitude,
            'latitude': delivery.subscriber.latitude
        })

    # WE SERIALIZE AND RETURN LIST INSTEAD OF MODELS 
    return jsonify({'deliveries': _list})


def _isCoordsNear(checkPointLng, checkPointLat, centerPoint, km):
    if checkPointLat is None or checkPointLng is None:
        return False
    
    if centerPoint.latitude in ["", None] or centerPoint.longitude in ["", None]:
        return False

    ky = 40000 / 360
    kx = cos(pi * float(centerPoint.latitude) / 180.0) * ky
    dx = abs(float(centerPoint.longitude) - float(checkPointLng)) * kx
    dy = abs(float(centerPoint.latitude) - float(checkPointLat)) * ky
    print("_isCoordsNear Result:", sqrt(dx * dx + dy * dy) <= km)
    return sqrt(dx * dx + dy * dy) <= km

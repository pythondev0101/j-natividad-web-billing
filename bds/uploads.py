from flask import current_app, redirect, render_template, request, flash, url_for
from flask_login import login_required
from app import CONTEXT, db
from bds import bp_bds
from bds.models import Area, SubArea, Subscriber
import os, csv, platform



@bp_bds.route('/upload/subscribers/csv', methods=['POST'])
@login_required
def upload_subscribers_csv():

    uploaded_file = request.files['csv_file']
    
    if uploaded_file.filename != '':
        file_path = os.path.join(current_app.config['UPLOAD_CSV_FOLDER'], uploaded_file.filename)
        
        if os.path.exists(file_path):
            flash("File exists!, (Rename the file then upload again)", 'error')
            return redirect(url_for('bp_bds.subscribers'))

        uploaded_file.save(file_path)

        try:
            with open(file_path, encoding = "ISO-8859-1") as f:
                csv_file = csv.reader(f)
                for _id,row in enumerate(csv_file):
                    if not _id == 0:
                        _area_name = row[0]
                        _sub_area_name = row[1]
                        area = Area.query.filter_by(name=_area_name).first()
                        sub_area = SubArea.query.filter_by(name=_sub_area_name).first()

                        new_area: Area
                        new_sub_area: SubArea

                        if area is None:
                            new_area = Area()
                            new_area.name = _area_name
                            new_area.description = None
                            db.session.add(new_area)
                            
                        if sub_area is None:
                            new_sub_area = SubArea()
                            new_sub_area.name = _sub_area_name
                            new_sub_area.description = None
                                
                            if area is None:
                                new_sub_area.area = new_area
                            else:
                                new_sub_area.area = area
                            
                            db.session.add(new_sub_area)

                        new = Subscriber()
                        new.contract_number = row[2]
                        new.fname = row[3]
                        new.lname = row[4]
                        new.address = row[6]
                        if sub_area is None:
                            new.sub_area = sub_area
                        else:
                            new.sub_area = sub_area

                        db.session.add(new)

                db.session.commit()
                flash("Subscribers uploaded!", 'success')
        
        except Exception as exc:
            if os.path.exists(file_path):
                os.remove(file_path)

            flash(str(exc), 'error')
            
    return redirect(url_for('bp_bds.subscribers'))

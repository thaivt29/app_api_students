from db import db
from model import Subject, Score
from flask import jsonify, request
from sqlalchemy.sql import func


def check_name(dt):
    name_sb = Subject.query.with_entities(Subject.name_subject).all()
    name_sbs = [name[0] for name in name_sb]
    if dt.get('name_subject') in name_sbs:
        return False
    return True

def check_id(dt):
    id_sb = Subject.query.with_entities(Subject.id).all()
    id_sbs = [id[0] for id in id_sb]
    if dt.get('id') in id_sbs:
        return False
    return True

def get_all_subject():
    data = Subject.query.all()
    list_subject = [sb.to_dict() for sb in data]
    return jsonify(list_subject)

def get_subject_id(id):
    sb = Subject.query.filter(func.lower(Subject.id) == id).first()
    if sb:
        return jsonify(sb.to_dict())
    return jsonify({'Message': 'Not Found Subject In DB'})

def insert_subject():
    data = request.get_json()
    try:
        if isinstance(data, dict):
            if ('name_subject' not in data) or ('id' not in data):
                return jsonify({'Erorr': 'Must Have Both Name And ID'})
            if check_name(data) == False:
                return jsonify({'Erorr': 'Duplicate Name_Subject'})
            subject = Subject(id = data['id'], name_subject = data['name_subject'])
            db.session.add(subject)
        elif isinstance(data, list):
            for item in data:
                if ('name_subject' not in item) or ('id' not in item):
                    return jsonify({'Erorr': 'Must Have Both Name And ID'})
                if check_name(item) == False:
                    return jsonify({'Erorr': 'Duplicate Name_Subject'})
                sb = Subject(id = item['id'], name_subject = item['name_subject'])
                db.session.add(sb)
        db.session.commit()
        return jsonify({'Insert Successful': data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'Erorr': str(e)})
    
def update_subject(id):
    subject = Subject.query.filter(Subject.id.like(id)).first()
    if subject:
        try:
            data = request.get_json()
            if check_name(data) == False:
                return jsonify({'Erorr': 'Duplicate Name_Subject'})
            subject.name_subject = data.get('name_subject', subject.name_subject)
            if check_id(data) == False:
                return jsonify({'Erorr': 'Duplicate Ma_MH'})
            subject.id = data.get('id', subject.id)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'Erorr': str(e)})
        return jsonify({'Message': 'Updated Successful'})
    return jsonify({'Message': 'Not Found Subject In DB'})


def delete_subject(id):
    id = id.lower()
    subject = Subject.query.filter(func.lower(Subject.id) == id).first()
    if subject:
        try:
            db.session.delete(subject)
        except Exception as e:
            return jsonify({'Erorr': str(e)})
        db.session.commit()
        return  jsonify({'Massage': 'Delete Successful'})
    return jsonify({'Message': 'Not Found Sb in DB'})


def select_all_score_subject(id):
    score = Score.query.filter(func.lower(Score.ma_mh) == id.lower()).all()
    if score:
        list_subject_score = [{'id': d.ma_hs, 'name': d.student.name, 
                                'ma_mh': d.ma_mh, 'score': d.score} for d in score]
        return jsonify(list_subject_score)
    return jsonify({'Message': 'Not Found Eny Subject_Score in DB'}), 404
    
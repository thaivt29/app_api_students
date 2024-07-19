from db import db
from model import Teacher , Subject
from flask import jsonify, request
from sqlalchemy import func

def check_mamh(t):
    mamh = Subject.query.with_entities(Subject.id).all()
    ma_mh = [ma[0] for ma in mamh]
    if t.get('ma_mh') not in ma_mh:
        return False
    return True


def get_all_teacher():
    data = Teacher.query.all()
    list_teacher = [Teach.to_dict() for Teach in data]
    return jsonify(list_teacher)


def get_teacher_id(id):
    teach = Teacher.query.get(id)
    if teach:
        return jsonify(teach.to_dict())
    return 'NOT FOUND TEACHER IN DB'


def insert_teacher():
    try:
        data = request.get_json()
        if isinstance(data, dict):
            if check_mamh(data):
                teach = Teacher(name = data['name'], birt_year = data.get('birt_year'), ma_mh = data['ma_mh'])
                db.session.add(teach)
            else:
                return jsonify({'Erorr': 'Conflict: Ma_mh Has Not In Subject Table'}), 400
        elif isinstance(data, list):
            for item in data:
                if check_mamh(item):
                    teach = Teacher(name = item['name'], birt_year = item.get('birt_year'), ma_mh = item['ma_mh'])
                    db.session.add(teach)
                else:
                    return jsonify({'Erorr': 'Conflict: Ma_mh Has Not In Subject Table'}), 400
        db.session.commit()
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        return 'Erorr'
    

def update_teacher(id):
    teach = Teacher.query.get(id)
    if teach:
        try:
            data = request.get_json()
            if check_mamh(data):
                teach.name = data.get('name', teach.name)
                teach.birt_year = data.get('birt_year', teach.birt_year)
                teach.ma_mh = data.get('ma_mh', teach.ma_mh)
            else:
                return jsonify({'Erorr': 'Conflict: Ma_mh Has Not In Subject Table'}), 400
        except Exception as e:
            print(e)
            return 'Erorr'
        db.session.commit()
        return jsonify(teach.to_dict())
    return "NOT FOUND TEACHER IN DB"
        
    

def delete_teacher(id):
    teach = Teacher.query.get(id)
    if teach:
        db.session.delete(teach)
        db.session.commit()
        return 'Deleted Successful'
    return 'NOT FOUND TEACHER IN DB'


def select_teacher_subject(name):
    teach = Teacher.query.filter(func.lower(Teacher.name) == name.lower()).all()
    if teach:
        teach_sb = [{'name': t.name, 'name_subject': t.subjects.name_subject} for t in teach]
        return jsonify(teach_sb)
    return jsonify({'Message': 'Not Found Eny Teacher in DB'}), 404
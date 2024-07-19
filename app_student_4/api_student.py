from db import db
from model import Students, Score
from flask import jsonify, request

def get_all_student():
    data = Students.query.all()
    list_student = [student.to_dict() for student in data]
    return jsonify(list_student)

def get_student_id(id):
    student = Students.query.get(id)
    if student:
        return jsonify(student.to_dict())
    return 'NOT FOUND STUDENT IN DB'

def insert_student():
    try:
        data = request.get_json()
        if isinstance(data, dict):
            student = Students(name=data['name'], birt_year=data.get('birt_year'), que=data.get('que'))
            db.session.add(student)
        elif isinstance(data, list):
            for item in data:
                student = Students(name=item['name'], birt_year=item.get('birt_year'), que=item.get('que'))
                db.session.add(student)
        db.session.commit()
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)})

def update_student(id):
    student = Students.query.get(id)
    if student:
        try:
            data = request.get_json()
            student.name = data.get('name', student.name)
            student.birt_year = data.get('birt_year', student.birt_year)
            student.que = data.get('que', student.que)
        except Exception as e:
            return str(e)
        db.session.commit()
        return jsonify(student.to_dict())
    return "NOT FOUND STUDENT IN DB"

def delete_student(id):
    student = Students.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return 'Deleted Successful'
    return 'NOT FOUND STUDENT IN DB'


def select_all_student_score(id):
    student = Score.query.filter(Score.ma_hs == id).all()
    if student:
        student_list_score  = [{'id': std.ma_hs, 'name': std.student.name, 
                                'name_subject': std.subjects.name_subject, 'score': std.score} for std in student]
        return jsonify(student_list_score)
    return jsonify({'Message': 'Not Found Eny Teacher in DB'})

from db import db
from model import Score, Students, Subject
from flask import jsonify, request


def check_info(dt):
    if ('ma_hs' not in dt) or ('ma_mh' not in dt):
        return False
    return True

def check_mahs_mamh(dt):
    mahs = Students.query.with_entities(Students.id).all()
    ma_hs = [ma[0] for ma in mahs]
    mamh = Subject.query.with_entities(Subject.id).all()
    ma_mh = [ma[0] for ma in mamh]
    if (dt['ma_hs'] not in ma_hs) or (dt['ma_mh'] not in ma_mh):
        return False
    return True


def get_all_score():
    data = Score.query.all()
    list_score = [score.to_dict() for score in data]
    return jsonify(list_score)


def get_score_id(ma_hs, ma_mh):
    data = Score.query.filter(Score.ma_hs == ma_hs, Score.ma_mh == ma_mh.upper()).first()
    if data:
        return jsonify(data.to_dict())
    return jsonify({'Message': 'Not Found In DB'}), 404



def insert_score():
    data = request.get_json()
    try:
        if isinstance(data, dict):
            if check_info(data):
                if check_mahs_mamh(data):
                    diem = Score(ma_hs = data['ma_hs'], ma_mh = data['ma_mh'], score = data.get('score'))
                    db.session.add(diem)
                else:
                    return jsonify({'Erorr': 'Conflict: Ma_hs or Ma_mh have not in DB '}), 400
            else:
                return jsonify({'Erorr': 'Must have Both Ma_hs and Ma_mh'}), 400
        elif isinstance(data, list):
            for item in data:
                if check_info(item):
                    if check_mahs_mamh(item):
                        diem = Score(ma_hs = item['ma_hs'], ma_mh = item['ma_mh'], score = item.get('score'))
                        db.session.add(diem)
                    else:
                        return jsonify({'Erorr': 'Conflict: Ma_hs or Ma_mh have not in DB '}), 400
                else:
                    return jsonify({'Erorr': 'Must have Both Ma_hs and Ma_mh'}), 400
        db.session.commit()
        return jsonify({'Insert Successful': data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'Erorr': str(e)}), 404
    

def update_score(ma_hs, ma_mh):
    data = Score.query.filter(Score.ma_hs == ma_hs, Score.ma_mh == ma_mh.upper()).first()
    if data:
        diem = request.get_json()
        data.score = diem.get('score', data.score)
        db.session.commit()
        return jsonify({'Updated Successful': data.to_dict()}), 200
    return jsonify({'Message': 'Not Found In DB'}), 404


def delete_score(ma_hs, ma_mh):
    data = Score.query.filter(Score.ma_hs == ma_hs, Score.ma_mh == ma_mh.upper()).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'Message': 'Delete Successful'}), 200
    return jsonify({'Message': 'Not Found In DB'}), 404
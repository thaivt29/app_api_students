from flask import Flask
import api_student as api_s
import api_teacher as api_t
import api_subject as api_sb
import api_score as api_score
from os import path
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db.init_app(app)


@app.route('/')
def check():
    return 'Hello My App'

@app.route('/student')
def api_get_all_student():
    return api_s.get_all_student()

@app.route('/student/<int:id>')
def api_get_student_id(id):
    return api_s.get_student_id(id)

@app.route('/insert/student', methods = ['POST'])
def api_insert_student():
    return api_s.insert_student()

@app.route('/update/student/<int:id>', methods = ['PUT'])
def api_update_student(id):
    return api_s.update_student(id)

@app.route('/delete/student/<int:id>', methods = ['DELETE'])
def api_delete_student(id):
    return api_s.delete_student(id)

@app.route('/student/score/<int:id>')
def api_select_all_student_score(id):
    return api_s.select_all_student_score(id)

@app.route('/teacher')
def api_get_all_teacher():
    return api_t.get_all_teacher()

@app.route('/teacher/<int:id>', methods = ['GET'])
def api_get_teacher_id(id):
    return api_t.get_teacher_id(id)

@app.route('/insert/teacher', methods = ['POST'])
def api_insert_teacher():
    return api_t.insert_teacher()

@app.route('/update/teacher/<int:id>', methods = ['PUT'])
def api_update_teacher(id):
    return api_t.update_teacher(id)

@app.route('/delete/teacher/<int:id>', methods = ['DELETE'])
def api_delete_teacher(id):
    return api_t.delete_teacher(id)

@app.route('/teacher/subject/<string:name>')
def api_select_teacher_subject(name):
    return api_t.select_teacher_subject(name)


@app.route('/subject')
def api_get_all_subject():
    return api_sb.get_all_subject()

@app.route('/subject/<string:id>', methods = ['GET'])
def api_get_subject_id(id):
    return api_sb.get_subject_id(id)

@app.route('/insert/subject', methods = ['POST'])
def api_insert_subject():
    return api_sb.insert_subject()

@app.route('/update/subject/<string:id>', methods = ['PUT'])
def api_update_subject(id):
    return api_sb.update_subject(id)

@app.route('/delete/subject/<string:id>', methods = ['DELETE'])
def api_delete_subject(id):
    return api_sb.delete_subject(id)

@app.route('/subject/score/<string:id>')
def api_select_all_score_subject(id):
    return api_sb.select_all_score_subject(id)

@app.route('/score')
def api_get_all_score():
    return api_score.get_all_score()

@app.route('/score/<int:ma_hs>/<string:ma_mh>', methods = ['GET'])
def api_get_score_id(ma_hs, ma_mh):
    return api_score.get_score_id(ma_hs, ma_mh)

@app.route('/insert/score', methods = ['POST'])
def api_insert_score():
    return api_score.insert_score()

@app.route('/update/score/<int:ma_hs>/<string:ma_mh>', methods = ['PUT'])
def api_update_score(ma_hs, ma_mh):
    return api_score.update_score(ma_hs, ma_mh)

@app.route('/delete/score/<int:ma_hs>/<string:ma_mh>', methods = ['DELETE'])
def api_delete_score(ma_hs, ma_mh):
    return api_score.delete_score(ma_hs, ma_mh)


if __name__ == '__main__':
    if not path.exists('student2.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

from db import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Subject(db.Model):
    id = Column(String(10), primary_key=True)
    name_subject = Column(String(50), nullable=False, unique=True)
    teachers = relationship('Teacher', backref='subjects', lazy=True)
    score_student = relationship('Score', backref='subjects', lazy=True)

    def to_dict(self):
        return {
                'id': self.id,
                'name_subject': self.name_subject
                }


class Students(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    birt_year = Column(Integer)
    que = Column(String(20))
    scores = relationship('Score', backref='student', lazy=True)

    def to_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'birt_year': self.birt_year,
                'que': self.que,
                }

class Score(db.Model):
    ma_hs = Column(Integer, ForeignKey(Students.id), primary_key=True)
    ma_mh = Column(String(10), ForeignKey(Subject.id), primary_key=True)
    score = Column(Float)

    def to_dict(self):
        return {
                'ma_hs': self.ma_hs,
                'ma_mh': self.ma_mh,
                'score': self.score
                }


class Teacher(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    birt_year = Column(Integer)
    ma_mh = Column(String(10), ForeignKey(Subject.id), nullable=False)

    def to_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'birt_year': self.birt_year,
                'ma_mh': self.ma_mh
        }

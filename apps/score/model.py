from exts import db


class Exam(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_name=db.Column(db.String(150),nullable=False)
    exam_datetime=db.Column(db.DateTime)
    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))
    clazz_id=db.Column(db.Integer,db.ForeignKey('clazz.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    s_scores=db.relationship('StudentScore',backref='exam')
    result=db.relationship('Result',backref='exam')

class StudentScore(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(50),nullable=False)
    score=db.Column(db.Float,nullable=False)
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.id'))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_num=db.Column(db.Integer,nullable=False)
    s_total=db.Column(db.Float,nullable=False) # 总分
    s_everage=db.Column(db.Float,nullable=False) # 平均分
    s_max=db.Column(db.Float,nullable=False) # 最高分
    s_min=db.Column(db.Float,nullable=False) # 最低分
    s_youxiu=db.Column(db.Float,nullable=False) # 优秀率
    s_hege=db.Column(db.Float,nullable=False) # 合格率
    down_60=db.Column(db.Integer,nullable=False) # 60分以下人数
    s60_70=db.Column(db.Integer,nullable=False) # 60分-70分人数
    s70_80 = db.Column(db.Integer, nullable=False)  # 70分-80分人数
    s80_90 = db.Column(db.Integer, nullable=False)  # 80分-90分人数
    s90_100 = db.Column(db.Integer, nullable=False)  # 90分-100分人数
    exam_id=db.Column(db.Integer,db.ForeignKey('exam.id'))
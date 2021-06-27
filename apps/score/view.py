import os
import random

from flask import render_template, request, jsonify, redirect, url_for, flash, session, g, abort, views

from flask import Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from apps.score.form import ExamForm, ScoreForm, ModifyScoreForm, AddScoreForm
from apps.score.model import StudentScore, Exam, Result
from apps.user.model import Course, Clazz
from exts import db
from settings import Config
import xlwings as xw
score_bp = Blueprint('score', __name__, url_prefix='/score')
allowed_suffix=['xls','xlsx']

@score_bp.route('/add_exam',methods=['GET','POST'])
@login_required
def add_exam():
    courses=Course.query.all()
    clazzs=Clazz.query.all()
    form=ExamForm()
    if request.method=='POST':
        if form.validate_on_submit():
            exam_name=form.exam_name.data
            course_id=form.course_id.data
            clazz_id=form.clazz_id.data
            user_id=form.user_id.data
            exam_datetime=form.exam_datetime.data

            exam=Exam()
            exam.exam_name=exam_name
            exam.course_id=course_id
            exam.clazz_id=clazz_id
            exam.user_id=user_id
            exam.exam_datetime=exam_datetime
            db.session.add(exam)
            db.session.commit()
            return redirect(url_for('score.index')+'?exam_id='+str(exam.id))
    return render_template('score/add_exam.html',form=form,courses=courses,clazzs=clazzs)

@score_bp.route('/',methods=['GET','POST'])
@login_required
def index():
    exam_id=int(request.args.get('exam_id'))
    exams=Exam.query.filter(Exam.user_id==current_user.id).all()
    form=ScoreForm()
    if request.method=='POST':
        if form.validate_on_submit():
            exam_id=form.exam_id.data
            s_file=form.s_file.data
            # s_file = secure_filename(s_file.filename)
            f_filename=s_file.filename.rsplit('.')[0]
            suffix=s_file.filename.rsplit('.')[-1]
            new_filename=f_filename+str(random.randint(100000,999999))+'.'+suffix
            file_path=os.path.join(Config.UPLOAD_FILE_DIR,new_filename)
            s_file.save(file_path)

            wb=xw.Book(file_path)
            sht=wb.sheets['sheet1']
            scores_list=sht.range('A3').expand().value
            for score in scores_list:
                fenshu=str(score[1])
                for f in fenshu:
                    if not (f.isdigit() or f=='.'):
                        print('------------------',f)
                        flash('模板数据错误')
                        return redirect(url_for('score.index'))
            for score in scores_list:
                s=StudentScore()
                s.name=score[0]
                s.score=score[1]
                s.exam_id=exam_id
                db.session.add(s)
                db.session.commit()
            return redirect(url_for('score.score_list')+'?exam_id='+str(exam_id))
    return render_template('score/index.html',exams=exams,form=form,exam_id=exam_id)

@score_bp.route('/exam')
def exam():
    exam_id=request.args.get('exam_id')
    if exam_id is None:
        abort(500)
    exam=Exam.query.get(exam_id)
    return jsonify(course=exam.course.cou_name,clazz=exam.clazz.c_name,teacher=exam.user.username,exam_datetime=exam.exam_datetime)


@score_bp.route('/score_list')
@login_required
def score_list():
    exams=Exam.query.filter(Exam.user_id==current_user.id)
    exam_id=request.args.get('exam_id')
    if exam_id is None:
        abort(500)
    s_scores=StudentScore.query.filter(StudentScore.exam_id==exam_id).order_by(StudentScore.id)
    return render_template('score/score_list.html',s_scores=s_scores,exams=exams)

@score_bp.route('/sel_score_list')
def sel_score_list():
    exam_id=request.args.get('exam_id')
    if exam_id is None:
        abort(500)
    s_scores=StudentScore.query.filter(StudentScore.exam_id==exam_id).order_by(StudentScore.id)
    score_list=[]
    for score in s_scores:
        score_dict = {}
        score_dict['id']=score.id
        score_dict['name']=score.name
        score_dict['score']=score.score
        score_dict['exam_id']=score.exam_id
        score_list.append(score_dict)
    return jsonify(score_list=score_list)

@score_bp.route('/del_score')
def del_score():
    score_id=request.args.get('score_id')
    if score_id is None:
        abort(500)
    score_id=int(score_id)
    score=StudentScore.query.get(score_id)
    s_scores=StudentScore.query.filter(StudentScore.exam_id==score.exam_id).order_by(StudentScore.id)
    db.session.delete(score)
    db.session.commit()
    score_list = []
    for score in s_scores:
        score_dict = {}
        score_dict['id'] = score.id
        score_dict['name'] = score.name
        score_dict['score'] = score.score
        score_list.append(score_dict)
    return jsonify(score_list=score_list)

class ModifyScoreView(views.MethodView):
    def get(self):
        score_id = request.args.get('score_id')
        if score_id is None:
            abort(500)
        score = StudentScore.query.get(score_id)
        form = ModifyScoreForm()
        form.id.data = score.id
        form.exam_id.data = score.exam_id
        form.name.data = score.name
        form.score.data = score.score
        return render_template('score/modify_score.html',form=form)

    def post(self):
        form=ModifyScoreForm()
        if form.validate_on_submit():
            id = form.id.data
            exam_id = form.exam_id.data
            name = form.name.data
            score = form.score.data

            s = StudentScore.query.get(id)
            s.exam_id = exam_id
            s.name = name
            s.score = score
            db.session.commit()
            return redirect(url_for('score.score_list') + '?exam_id=' + str(exam_id))
        return render_template('score/modify_score.html',form=form)

score_bp.add_url_rule('/modify_score',endpoint='modify_score',view_func=ModifyScoreView.as_view('get'))
score_bp.add_url_rule('/save_modify_score',endpoint='s_modify_score',view_func=ModifyScoreView.as_view('post'))

class AddScoreView(views.MethodView):
    def get(self):
        exam_id = request.args.get('exam_id')
        if exam_id is None:
            abort(500)
        form = AddScoreForm()
        return render_template('score/add_score.html', exam_id=exam_id, form=form)

    def post(self):
        form=AddScoreForm()
        if form.validate_on_submit():
            exam_id = form.exam_id.data
            name = form.name.data
            score = form.score.data

            s = StudentScore()
            s.name = name
            s.score = score
            s.exam_id = exam_id
            db.session.add(s)
            db.session.commit()
            return redirect(url_for('score.score_list') + '?exam_id=' + str(exam_id))
        return render_template('score/add_score.html', exam_id=form.exam_id.data, form=form)

score_bp.add_url_rule('/add_score',endpoint='add_score',view_func=AddScoreView.as_view('get'))
score_bp.add_url_rule('/save_add_score',endpoint='s_add_score',view_func=AddScoreView.as_view('post'))

@score_bp.route('/tongji')
def tongji():
    exam_id=request.args.get('exam_id')
    if exam_id is None:
        abort(500)
    youxiulv=int(request.args.get('youxiulv'))
    results=Result.query.filter(Result.exam_id==exam_id).all()
    scores=StudentScore.query.filter(StudentScore.exam_id==exam_id).all()
    s_num=len(scores)        # 考试人数
    s_total=0
    score_list=[]
    hege_num=0
    youxiu_num=0
    num60_70=0
    num70_80 = 0
    num80_90=0
    num90_100=0
    for s_score in scores:
        if s_score.score>60:
            hege_num+=1
        if s_score.score>=youxiulv:
            youxiu_num+=1
        if s_score.score>=60 and s_score.score<70:
            num60_70+=1           # 60-70人数
        if s_score.score>=70 and s_score.score<80:
            num70_80+=1           # 70-80人数
        if s_score.score>=80 and s_score.score<90:
            num80_90+=1           # 80-90人数
        if s_score.score>=90:
            num90_100+=1          # 90-100人数
        score_list.append(s_score.score)
        s_total+=s_score.score   # 班级总分
    s_everage=s_total/s_num      # 平均分
    s_max=max(score_list)        # 最高分
    s_min=min(score_list)        # 最低分
    s_hege=hege_num/s_num        # 合格率
    s_youxiu=youxiu_num/s_num    # 优秀率
    down_60=s_num-hege_num       # 60分以下人数
    return jsonify(s_num=s_num,s_total=s_total,s_everage=s_everage,
                   s_youxiu=s_youxiu,s_hege=s_hege,s_max=s_max,
                   s_min=s_min,num60_70=num60_70,num70_80=num70_80,
                   num80_90=num80_90,num90_100=num90_100,down_60=down_60)

@score_bp.route('/save_tongji')
def save_tongji():
    s_num=request.args.get('s_num')
    if s_num is None:
        abort(500)
    s_total=request.args.get('s_total')
    s_everage=request.args.get('s_everage')
    s_youxiu=request.args.get('s_youxiu')
    s_hege=request.args.get('s_hege')
    s_max=request.args.get('s_max')
    s_min=request.args.get('s_min')
    down_60=request.args.get('down_60')
    num60_70=request.args.get('num60_70')
    num70_80=request.args.get('num70_80')
    num80_90=request.args.get('num80_90')
    num90_100=request.args.get('num90_100')
    exam_id=request.args.get('exam_id')
    result=Result.query.filter(Result.exam_id==exam_id).first()
    if result:
        result.s_num=s_num
        result.s_total=s_total
        result.s_everage=s_everage
        result.s_youxiu=s_youxiu
        result.s_hege=s_hege
        result.s_max=s_max
        result.s_min=s_min
        result.down_60=down_60
        result.s60_70=num60_70
        result.s70_80=num70_80
        result.s80_90=num80_90
        result.s90_100=num90_100
        result.exam_id=exam_id
        db.session.commit()
        return jsonify(msg='覆盖保存成功')
    r=Result()
    r.s_num=s_num
    r.s_total=s_total
    r.s_everage=s_everage
    r.s_youxiu=s_youxiu
    r.s_hege=s_hege
    r.s_max=s_max
    r.s_min=s_min
    r.down_60=down_60
    r.s60_70=num60_70
    r.s70_80=num70_80
    r.s80_90=num80_90
    r.s90_100=num90_100
    r.exam_id=exam_id
    db.session.add(r)
    db.session.commit()
    return jsonify(msg='保存成功')








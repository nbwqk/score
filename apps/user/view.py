from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, abort, views
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from apps.user.form import UserRegisterForm, LoginForm, AddUserForm, ModifyUserForm
from apps.user.model import User, Clazz, Course
from exts import db, login_manager

user_bp=Blueprint('user',__name__,url_prefix='/user')

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

@user_bp.route('/register',methods=['GET','POST'])
def register():
    form=UserRegisterForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=form.username.data
            password=form.password.data
            phone=form.phone.data
            email=form.email.data

            u=User()
            u.username=username
            u.password=generate_password_hash(password)
            u.phone=phone
            u.email=email
            db.session.add(u)
            db.session.commit()
            login_user(u)
            flash(message='注册成功！')
            return redirect(url_for('score.add_exam'))
    return render_template('user/register.html',form=form)

@user_bp.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            phone=form.phone.data
            password=form.password.data
            user=User.query.filter(User.phone==phone).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user)
                    flash('登录成功！')
                    return redirect(url_for('score.add_exam'))
            flash('登录失败！')
    return render_template('user/login.html',form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user_bp.route('/check_phone')
def check_phone():
    phone=request.args.get('phone')
    if phone is None:
        abort(500)
    user=User.query.filter(User.phone==phone).first()
    if user:
        return jsonify(code=400,msg='电话已注册，请更换！')
    return jsonify(code=200)

def login_required_admin(func):
    @login_required
    def inner(*args,**kwargs):
        if current_user.isadmin==1:
            return func(*args,**kwargs)
        else:
            flash('不是管理员，登录失败！')
            return redirect(url_for('user.login'))
    return inner

@user_bp.route('/admin')
@login_required_admin
def admin():
    users=User.query.all()
    return render_template('user/admin.html',users=users)

@user_bp.route('/m_clazz')
def m_clazz():
    clazzs=Clazz.query.order_by(Clazz.id).all()
    clazz_list=[]
    for clazz in clazzs:
        clazz_dict = {}
        clazz_dict['id']=clazz.id
        clazz_dict['c_name']=clazz.c_name
        clazz_list.append(clazz_dict)
    return jsonify(clazz_list=clazz_list)

@user_bp.route('/add_clazz')
def add_clazz():
    c_name=request.args.get('c_name')
    if c_name is None:
        abort(500)
    c=Clazz.query.filter(Clazz.c_name==c_name).first()
    if c:
        return jsonify(code=400,msg='班级已存在，请更换！')
    c=Clazz()
    c.c_name=c_name
    db.session.add(c)
    db.session.commit()

    clazzs = Clazz.query.order_by(Clazz.id).all()
    clazz_list = []
    for clazz in clazzs:
        clazz_dict = {}
        clazz_dict['id'] = clazz.id
        clazz_dict['c_name'] = clazz.c_name
        clazz_list.append(clazz_dict)
    return jsonify(clazz_list=clazz_list)

@user_bp.route('/del_clazz')
def del_clazz():
    clazz_id=request.args.get('clazz_id')
    if clazz_id is None:
        abort(500)
    c=Clazz.query.get(clazz_id)
    if c.exams:
        return jsonify(code=400,msg='这个班级有记录考试，请先删除考试！')
    db.session.delete(c)
    db.session.commit()

    clazzs = Clazz.query.order_by(Clazz.id).all()
    clazz_list = []
    for clazz in clazzs:
        clazz_dict = {}
        clazz_dict['id'] = clazz.id
        clazz_dict['c_name'] = clazz.c_name
        clazz_list.append(clazz_dict)
    return jsonify(clazz_list=clazz_list)

@user_bp.route('/modify_clazz')
def modify_clazz():
    clazz_id=request.args.get('clazz_id')
    c_name=request.args.get('c_name')
    if clazz_id is None or c_name is None:
        abort(500)
    c=Clazz.query.get(clazz_id)
    c.c_name=c_name
    db.session.commit()

    clazzs = Clazz.query.order_by(Clazz.id).all()
    clazz_list = []
    for clazz in clazzs:
        clazz_dict = {}
        clazz_dict['id'] = clazz.id
        clazz_dict['c_name'] = clazz.c_name
        clazz_list.append(clazz_dict)
    return jsonify(clazz_list=clazz_list)

@user_bp.route('/m_course')
def m_course():
    courses=Course.query.order_by(Course.id).all()
    course_list=[]
    for course in courses:
        course_dict = {}
        course_dict['id']=course.id
        course_dict['cou_name']=course.cou_name
        course_list.append(course_dict)
    return jsonify(course_list=course_list)

@user_bp.route('/add_course')
def add_course():
    cou_name=request.args.get('cou_name')
    if cou_name is None:
        abort(500)
    c=Course.query.filter(Course.cou_name==cou_name).first()
    if c:
        return jsonify(code=400,msg='课程已存在，请更换！')
    c=Course()
    c.cou_name=cou_name
    db.session.add(c)
    db.session.commit()

    courses = Course.query.order_by(Course.id).all()
    course_list = []
    for course in courses:
        course_dict = {}
        course_dict['id'] = course.id
        course_dict['cou_name'] = course.cou_name
        course_list.append(course_dict)
    return jsonify(course_list=course_list)

@user_bp.route('/del_course')
def del_course():
    course_id = request.args.get('course_id')
    if course_id is None:
        abort(500)
    c = Course.query.get(course_id)
    if c.exams:
        return jsonify(code=400, msg='这个课程有记录考试，请先删除考试！')
    db.session.delete(c)
    db.session.commit()

    courses = Course.query.order_by(Course.id).all()
    course_list = []
    for course in courses:
        course_dict = {}
        course_dict['id'] = course.id
        course_dict['cou_name'] = course.cou_name
        course_list.append(course_dict)
    return jsonify(course_list=course_list)

@user_bp.route('/modify_course')
def modify_course():
    course_id=request.args.get('course_id')
    cou_name=request.args.get('cou_name')
    if course_id is None or cou_name is None:
        abort(500)
    c=Course.query.get(course_id)
    c.cou_name=cou_name
    db.session.commit()

    courses = Course.query.order_by(Course.id).all()
    course_list = []
    for course in courses:
        course_dict = {}
        course_dict['id'] = course.id
        course_dict['cou_name'] = course.cou_name
        course_list.append(course_dict)
    return jsonify(course_list=course_list)

@user_bp.route('/m_user')
def m_user():
    users=User.query.order_by(-User.id).all()
    user_list=[]
    for user in users:
        user_dict = {}
        user_dict['id']=user.id
        user_dict['username']=user.username
        user_dict['phone']=user.phone
        user_dict['email']=user.email
        user_dict['isforbid']=user.isforbid
        user_dict['isadmin']=user.isadmin
        user_list.append(user_dict)
    return jsonify(user_list=user_list)

@user_bp.route('/add_user',methods=['GET','POST'])
def add_user():
    form=AddUserForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=form.username.data
            password=form.password.data
            phone=form.phone.data
            email=form.email.data

            u=User()
            u.username=username
            u.password=generate_password_hash(password)
            u.phone=phone
            u.email=email
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('user.admin'))
    return render_template('user/add_user.html',form=form)

class ModifyUserView(views.MethodView):
    def get(self):
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)
        form = ModifyUserForm()
        form.user_id.data=user.id
        form.username.data = user.username
        form.phone.data = user.phone
        form.email.data = user.email
        return render_template('user/modify_user.html',form=form)

    def post(self):
        form = ModifyUserForm()
        if form.validate_on_submit():
            user_id=form.user_id.data
            user=User.query.get(user_id)
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.phone = form.phone.data
            user.email = form.email.data

            db.session.commit()
            return redirect(url_for('user.admin'))
        return render_template('user/modify_user.html',form=form)

user_bp.add_url_rule('/list_user',view_func=ModifyUserView.as_view('get'))
user_bp.add_url_rule('/modify_user',view_func=ModifyUserView.as_view('post'))

@user_bp.route('/del_user')
def del_user():
    user_id=request.args.get('user_id')
    if user_id is None:
        abort(500)
    user=User.query.get(user_id)
    if user.exams:
        return jsonify(code=400,msg='该用户有考试记录，请先删除考试！')
    db.session.delete(user)
    db.session.commit()

    users = User.query.all()
    user_list = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['username'] = user.username
        user_dict['phone'] = user.phone
        user_dict['email'] = user.email
        user_dict['isforbid'] = user.isforbid
        user_dict['isadmin'] = user.isadmin
        user_list.append(user_dict)
    return jsonify(user_list=user_list)

@user_bp.route('/forbid')
def forbid_user():
    user_id=request.args.get('user_id')
    if user_id is None:
        abort(500)
    user=User.query.get(user_id)
    if user.isforbid==0:
        user.isforbid=1
    else:
        user.isforbid=0
    db.session.commit()

    users = User.query.all()
    user_list = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['username'] = user.username
        user_dict['phone'] = user.phone
        user_dict['email'] = user.email
        user_dict['isforbid'] = user.isforbid
        user_dict['isadmin'] = user.isadmin
        user_list.append(user_dict)
    return jsonify(user_list=user_list)

@user_bp.route('/isadmin')
def isadmin():
    user_id=request.args.get('user_id')
    if user_id is None:
        abort(500)
    user=User.query.get(user_id)
    if user.isadmin==0:
        user.isadmin=1
    else:
        user.isadmin=0
    db.session.commit()

    users = User.query.all()
    user_list = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['username'] = user.username
        user_dict['phone'] = user.phone
        user_dict['email'] = user.email
        user_dict['isforbid'] = user.isforbid
        user_dict['isadmin'] = user.isadmin
        user_list.append(user_dict)
    return jsonify(user_list=user_list)








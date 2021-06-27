from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, FloatField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, ValidationError


class ExamForm(FlaskForm):
    exam_name=StringField(validators=[DataRequired(message='该数据必须填写'),Length(max=50,message='考试名称不能多于50位')])
    course_id = IntegerField(validators=[DataRequired(message='该数据必须填写')])
    clazz_id = IntegerField(validators=[DataRequired(message='该数据必须填写')])
    user_id = IntegerField(validators=[DataRequired(message='该数据必须填写')])
    exam_datetime= StringField(validators=[DataRequired(message='该数据必须填写')])

class ScoreForm(FlaskForm):
    exam_id=IntegerField(validators=[DataRequired(message='该数据必须填写')])
    s_file=FileField(validators=[DataRequired(message='该模板必须上传')])

    def validate_s_file(self,data):
        suffix=data.data.filename.rsplit('.')[-1]
        allowed_suffix=['xls','xlsx']
        if suffix not in allowed_suffix:
            raise ValidationError('文件格式错误')

class ModifyScoreForm(FlaskForm):
    id=IntegerField(validators=[DataRequired(message='该数据必须填写')])
    exam_id=IntegerField(validators=[DataRequired(message='该数据必须填写')])
    name=StringField(validators=[DataRequired(message='该数据必须填写')])
    score=StringField(validators=[DataRequired(message='该数据必须填写')])

class AddScoreForm(FlaskForm):
    exam_id=IntegerField(validators=[DataRequired(message='该数据必须填写')])
    name=StringField(validators=[DataRequired(message='该数据必须填写')])
    score=StringField(validators=[DataRequired(message='该数据必须填写')])
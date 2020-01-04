from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Department, Role, Report

class ReportForm(FlaskForm):
    name = StringField('Tên báo cáo', validators=[DataRequired()])
    report_file = FileField('File báo cáo', validators=[FileRequired()])
    submit = SubmitField('Nộp')

class EditInformation(FlaskForm):
    gender = SelectField('Giới tính', choices = [('male', 'Nam'), ('female', 'Nữ')])
    birthday = DateTimeField('Ngày sinh', format='%d/%m/%Y', validators=[DataRequired()])
    mobile = StringField('Số điện thoại', validators=[DataRequired()])
    education = StringField('Học vấn')
    education_place = StringField('Nơi đào tạo')
    entry_date = DateTimeField('Ngày vào công ty', format='%d/%m/%Y')
    official_date = DateTimeField('Ngày chính thức', format='%d/%m/%Y')
    address = StringField('Địa chỉ')
    submit = SubmitField('Sửa thông tin')

class Set_Password(FlaskForm):
    old_password = PasswordField('Mật khẩu cũ', validators=[DataRequired()])
    password = PasswordField('Mật khẩu mới', validators=[
                             EqualTo('confirm_password'), DataRequired()])
    confirm_password = PasswordField('Xác nhận mật khẩu')

class EditReportForm(FlaskForm):
    name = StringField('Tên báo cáo', validators=[DataRequired()])
    submit = SubmitField('Nộp')

class CVForm(FlaskForm):
    name = StringField('Họ và tên', validators=[DataRequired()])
    gender = SelectField('Giới tính', choices = [('Nam', 'Nam'), ('Nữ', 'Nữ')])
    birthday = DateTimeField('Ngày sinh (VD 01/01/1994)', format='%d/%m/%Y', validators=[DataRequired()])
    mobile = StringField('Số điện thoại', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    education = StringField('Học vấn')
    education_place = StringField('Nơi đào tạo')
    apply_position = StringField('Vị trí ứng tuyển', validators=[DataRequired()])
    cv_file = FileField('File CV', validators=[FileAllowed (['pdf'], 'Chỉ sử dụng file .pdf')])
    submit = SubmitField('Nộp hồ sơ')
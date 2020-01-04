from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash


from app.models import Employee


class RegistrationForm(FlaskForm):
    email = StringField('Địa chỉ email', validators=[Email(), DataRequired()])
    username = StringField('Tên người dùng', validators=[DataRequired()])
    first_name = StringField('Tên', validators=[DataRequired()])
    last_name = StringField('Họ và đệm', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[
                             EqualTo('confirm_password'), DataRequired()])
    confirm_password = PasswordField('Xác nhận mật khẩu')
    submit = SubmitField('Đăng ký')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email đã được sử dụng.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Tên người dùng đã được sử dụng.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

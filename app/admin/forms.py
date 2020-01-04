from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, DateTimeField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Department, Role


class DepartmentForm(FlaskForm):
    name = StringField('Tên phòng ban', validators=[DataRequired()])
    description = StringField('Miêu tả')
    submit = SubmitField('Thêm')

class RoleForm(FlaskForm):
    name = StringField('Chức vụ', validators=[DataRequired()])
    description = StringField('Miêu tả')
    manage = QuerySelectField('Quản lý', query_factory=lambda: Role.query.all(),
                            get_label="name", allow_blank=True)
    only_manage_department = BooleanField('Chỉ quản lý trong phòng')
    submit = SubmitField('Thêm')

class EmployeeAssignForm(FlaskForm):
    department = QuerySelectField('Phòng ban', query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField('Chức vụ', query_factory=lambda: Role.query.all(),
                            get_label="name")
    position = StringField('Vị trí')
    submit = SubmitField('Lưu')

class SearchEmployeeForm(FlaskForm):
    choices = SelectField('Thuộc tính nhân viên cần tìm kiếm', choices=[('name', 'Tên'),
               ('email', 'Email'),
               ('mobile', 'Điện thoại'), ('department', 'Phòng ban'), ('role', 'Chức vụ')])
    search = StringField('Chuỗi tìm kiếm')
    submit = SubmitField('Tìm kiếm')

class CVEditForm(FlaskForm):
    name = StringField('Họ và tên', validators=[DataRequired()])
    gender = SelectField('Giới tính', choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')])
    birthday = DateTimeField('Ngày sinh (VD 01/01/1994)', format='%d/%m/%Y', validators=[DataRequired()])
    mobile = StringField('Số điện thoại', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    education = StringField('Học vấn')
    education_place = StringField('Nơi đào tạo')
    apply_position = StringField('Vị trí ứng tuyển', validators=[DataRequired()])
    status = SelectField('Trạng thái', choices=[('Đang xử lý', 'Đang xử lý'), ('Đã duyệt', 'Đã duyệt'), ('Chờ phỏng vấn', 'Chờ phỏng vấn'), ('Đã xong','Đã xong')])
    submit = SubmitField('Sửa hồ sơ')

class EditContactForm(FlaskForm):
    first_name = StringField('Tên')
    last_name = StringField('Họ và tên đệm')
    gender = SelectField('Giới tính', choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')])
    birthday = DateTimeField('Ngày sinh (VD 01/01/1994)', format='%d/%m/%Y')
    mobile = StringField('Số điện thoại', validators=[DataRequired()])
    education = StringField('Học vấn')
    education_place = StringField('Nơi đào tạo')
    entry_date = DateTimeField('Ngày vào công ty', format='%d/%m/%Y')
    official_date = DateTimeField('Ngày chính thức', format='%d/%m/%Y')
    address = StringField('Địa chỉ')
    submit = SubmitField('Sửa thông tin')

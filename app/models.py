from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from werkzeug import secure_filename
from flask_wtf.file import FileField

from app import db, login_manager
import enum


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(10))
    position = db.Column(db.String(30))
    education = db.Column(db.String(30))
    education_place = db.Column(db.String(30))
    entry_date = db.Column(db.Date)
    official_date = db.Column(db.Date)
    address = db.Column(db.String(50))
    reports = db.relationship('Report', backref='employee',
                                lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    manage_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    manage = db.relationship('Role', backref=('manager'), remote_side=[id])
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')
    is_admin = db.Column(db.Boolean, default=False)
    only_manage_department = db.Column(db.Boolean)

    def __repr__(self):
        return '{}'.format(self.name)


class Report(db.Model):
    """
    Create a Report table
    """

    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    report_file = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    def __repr__(self):
        return '{}'.format(self.name)

class CV_Information(db.Model):
    """
    Create a CV Information table
    """
    __tablename__ = 'cv_inform'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(10))
    education = db.Column(db.String(30))
    education_place = db.Column(db.String(30))
    apply_position = db.Column(db.String(30))
    email = db.Column(db.String(60), index=True)
    cv_file = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(20))

    def __repr__(self):
        return '{}'.format(self.name)





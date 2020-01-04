import os
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import Department, Role, Employee

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

def addTruongphong():
    role = Role(name='Trưởng phòng', description='Quản lý nhân viên')
    db.session.add(role)
    db.session.commit()


if __name__ == '__main__':
    # app.run()
    addTruongphong()


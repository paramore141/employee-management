import datetime
import os

from flask import abort, flash, redirect, render_template, url_for, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask import current_app
from app.home.forms import ReportForm, EditReportForm, CVForm, EditInformation
from app.home import home
from app import db
from app.models import Report, Employee, Role, Department, CV_Information


@home.route('/')
def homepage():

    return render_template('home/index.html', title='Quản lý nhân sự')


@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title='Trang chủ')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Trang chủ admin')


@home.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('home/profilepage.html', title='Hồ sơ cá nhân')


@home.route('/recruitment')
@login_required
def recruitment():
    # List all the applications
    cvs = CV_Information.query.all()
    return render_template('home/recruitment.html', cvs=cvs, title='Danh sách ứng viên')


@home.route('/apply')
def apply():
    cvs = CV_Information.query.all()
    return render_template('home/apply.html', cvs=cvs, title='Tuyển dụng')

@home.route('/apply/add', methods=['GET', 'POST'])
def add_apply():
    form = CVForm()
    if form.validate_on_submit():

        cv = CV_Information(name=form.name.data,
                        gender=form.gender.data,
                        birthday=form.birthday.data,
                        mobile=form.mobile.data,
                        education=form.education.data,
                        education_place=form.education_place.data,
                        apply_position=form.apply_position.data,
                        email=form.email.data,
                        cv_file=secure_filename(form.cv_file.data.filename))
        f = form.cv_file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        try:
            # add report to the database
            db.session.add(cv)
            db.session.commit()
            flash('Đã ứng tuyển thành công.')
        except:
            # in case report file already exists
            flash('Lỗi: Tên file đã tồn tại.')

        # redirect to the reports page
        return redirect(url_for('home.apply'))

    # load report template
    return render_template('home/apply_add.html', form=form, title='Nộp đơn ứng tuyển')

@home.route('/reports')
@login_required
def list_reports():
    reports = Report.query.filter(Report.employee == current_user).all()
    if current_user.role.only_manage_department:
        employee_reports = Report.query.join(Employee).join(Role).filter(current_user.role.manage_id == Role.id).filter(current_user.department == Employee.department).all()
    else:
        employee_reports = Report.query.join(Employee).join(Role).filter(current_user.role.manage_id == Role.id).all()

    return render_template('home/reports.html',
                           reports=reports, employee_reports=employee_reports, title='Danh sách báo cáo')


@home.route('/reports/add', methods=['GET', 'POST'])
@login_required
def add_report():
    """
    Add report to the database
    """
    add_report = True

    form = ReportForm()
    if form.validate_on_submit():

        report = Report(name=form.name.data,
                        report_file = secure_filename(form.report_file.data.filename),
                        employee=current_user)
        f = form.report_file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        try:
            # add report to the database
            db.session.add(report)
            db.session.commit()
            flash('Đã thêm báo cáo thành công.')
        except:
            # in case report file already exists
            flash('Lỗi: Tên file báo cáo đã tồn tại.')

        # redirect to the reports page
        return redirect(url_for('home.list_reports'))

    # load report template
    return render_template('home/report.html', add_report=add_report,
                           form=form, title='Thêm báo cáo')

@home.route('/reports/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_report(id):
    """
    Edit a report
    """
    add_report = False

    report = Report.query.get_or_404(id)
    form = EditReportForm(obj=report)
    if form.validate_on_submit():
        report.name = form.name.data
        db.session.add(report)
        db.session.commit()
        flash('Đã sửa tên báo cáo thành công.')

        # redirect to the roles page
        return redirect(url_for('home.list_reports'))

    form.name.data = report.name
    return render_template('home/report.html', action='add',
                           add_report=add_report,
                           form=form, title="Sửa tên báo cáo")

@home.route('/reports/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_report(id):
    """
    Delete a report from the database
    """
    report = Report.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    flash('Đã xóa báo cáo thành công.')

    # redirect to the roles page
    return redirect(url_for('home.list_reports'))

    return render_template(title="Xóa báo cáo")



@home.route('/downloads/<path:filename>')
@login_required
def download_file(filename):
    # Download file
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

@home.route('/contacts')
@login_required
def list_contacts():
    """
    List all contacts
    """
    employees = Employee.query.all()
    return render_template('home/contacts.html',
                           employees=employees, title='Nhân viên')

@home.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_information():

    profile = Employee.query.get(current_user.id)

    form = EditInformation(obj=profile)
    if form.validate_on_submit():
        profile.gender = form.gender.data
        profile.birthday = form.birthday.data
        profile.mobile = form.mobile.data
        profile.education = form.education.data
        profile.education_place = form.education_place.data
        profile.entry_date = form.entry_date.data
        profile.official_date = form.official_date.data
        profile.address = form.address.data

        db.session.add(profile)
        db.session.commit()
        flash('Đã sửa thông tin thành công.')

        # redirect to the roles page
        return redirect(url_for('home.profile'))

    return render_template('home/profile_edit.html',
                           profile=profile, form=form,
                           title='Sửa thông tin cá nhân')
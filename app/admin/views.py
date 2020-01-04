from flask import abort, flash, redirect, render_template, url_for, current_app, send_from_directory
from flask_login import current_user, login_required

from app.admin import admin
from app.admin.forms import DepartmentForm, RoleForm, EmployeeAssignForm, SearchEmployeeForm, CVEditForm, \
    EditContactForm
from app import db
from app.models import Department, Role, Employee, Report, CV_Information


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html',
                           departments=departments, title="Phòng ban")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    check_admin()
    add_department = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('Đã thêm phòng ban thành công.')
        except:
            # in case department name already exists
            flash('Lỗi: Tên phòng ban đã tồn tại.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="add",
                           add_department=add_department, form=form,
                           title="Thêm phòng ban")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('Đã sửa phòng ban thành công.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="add",
                           add_department=add_department, form=form,
                           department=department, title="Sửa phòng ban")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('Đã xóa phòng ban thành công.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Xóa phòng ban")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Chức vụ')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data,
                    manage=form.manage.data,
                    only_manage_department=form.only_manage_department.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('Đã thêm chức vụ thành công.')
        except:
            # in case role name already exists
            flash('Lỗi: Tên chức vụ đã tồn tại.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Thêm chức vụ')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        role.manage = form.manage.data
        role.only_manage_department = form.only_manage_department.data
        db.session.add(role)
        db.session.commit()
        flash('Đã sửa chức vụ thành công.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Sửa chức vụ")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('Đã xóa chức vụ thành công.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Xóa chức vụ")


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Nhân viên')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        employee.position = form.position.data
        db.session.add(employee)
        db.session.commit()
        flash('Đã sửa nhân viên thành công.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Sửa nhân viên')


@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    db.session.delete(employee)
    db.session.commit()
    flash('Đã xóa nhân viên thành công.')

    # redirect to the roles page
    return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Xóa nhân viên')


@admin.route('/employees/search', defaults={'search': ''}, methods=['GET', 'POST'])
@admin.route('/employees/search/<search>', methods=['GET', 'POST'])
@login_required
def search_employee(search):
    # Search employees
    check_admin()
    employees = []
    form = SearchEmployeeForm()
    if form.validate_on_submit():
        search = form.search.data
        choices = form.choices.data
        if search == '':
            employees = Employee.query.all()
        else:
            if choices == 'name':
                employees = Employee.query.filter(Employee.name.contains(search)).all()
            elif choices == 'email':
                employees = Employee.query.filter(Employee.email.contains(search)).all()
            elif choices == 'mobile':
                employees = Employee.query.filter(Employee.mobile.contains(search)).all()
            elif choices == 'department':
                employees = Employee.query.join(Department).filter(Department.name.contains(search)).all()
            else:
                employees = Employee.query.join(Role).filter(Role.name.contains(search)).all()
        if not employees:
            flash('Không tìm thấy kết quả')
            return redirect(url_for('admin.search_employee'))

    return render_template('admin/employees/search_employee.html',
                           form=form, employees = employees, title='Tìm kiếm nhân viên')



# --------------------------------------------------#


@admin.route('/reports')
@login_required
def list_reports():
    check_admin()
    """
    List all reports    
    """
    reports = Report.query.all()
    return render_template('admin/reports/reports.html',
                           reports=reports, title='Báo cáo')


@admin.route('/reports/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_report(id):
    """
    Delete a report from the database
    """
    check_admin()

    report = Report.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    flash('Đã xóa báo cáo thành công.')

    # redirect to the roles page
    return redirect(url_for('admin.list_reports'))

    return render_template(title="Xóa báo cáo")


@admin.route('/downloads/<path:filename>')
@login_required
def download_file(filename):
    check_admin()
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


@admin.route('/recruitments')
@login_required
def list_recruitments():
    check_admin()
    # List all applications
    cvs = CV_Information.query.all()
    return render_template('admin/recruitment/recruitments.html',
                           cvs=cvs, title='Tuyển dụng')


@admin.route('/recruitments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recruitment(id):
    check_admin()

    cv = CV_Information.query.get_or_404(id)

    form = CVEditForm(obj=cv)
    if form.validate_on_submit():
        cv.name = form.name.data
        cv.gender = form.gender.data
        cv.birthday = form.birthday.data
        cv.mobile = form.mobile.data
        cv.education = form.education.data
        cv.education_place = form.education_place.data
        cv.apply_position = form.apply_position.data
        cv.email = form.email.data
        cv.status = form.status.data

        db.session.add(cv)
        db.session.commit()
        flash('Đã sửa đơn ứng tuyển thành công.')

        # redirect to the roles page
        return redirect(url_for('admin.list_recruitments'))

    return render_template('admin/recruitment/recruitment.html',
                           cv=cv, form=form,
                           title='Sửa hồ sơ ứng tuyển')

@admin.route('/recruitments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recruitment(id):
    """
    Delete a report from the database
    """
    check_admin()

    cv = CV_Information.query.get_or_404(id)
    db.session.delete(cv)
    db.session.commit()
    flash('Đã xóa đơn ứng tuyển thành công.')

    # redirect to the roles page
    return redirect(url_for('admin.list_recruitments'))

    return render_template(title="Xóa đơn ứng tuyển")


@admin.route('/contacts')
@login_required
def list_contacts():
    """
    List all employees
    """
    check_admin()

    contacts = Employee.query.all()
    return render_template('admin/contacts/contacts.html',
                           contacts=contacts, title='Danh bạ nhân viên')


@admin.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    contact = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if contact.is_admin:
        abort(403)

    form = EditContactForm(obj=contact)
    if form.validate_on_submit():
        contact.first_name = form.first_name.data
        contact.last_name = form.last_name.data
        contact.name = form.last_name.data + form.first_name.data
        contact.gender = form.gender.data
        contact.birthday = form.birthday.data
        contact.mobile = form.mobile.data
        contact.education = form.education.data
        contact.education_place = form.education_place.data
        contact.entry_date = form.entry_date.data
        contact.official_date = form.official_date.data
        contact.address = form.address.data

        db.session.add(contact)
        db.session.commit()
        flash('Đã sửa thông tin thành công.')

        # redirect to the roles page
        return redirect(url_for('admin.list_contacts'))

    return render_template('admin/contacts/contact.html',
                           contact=contact, form=form,
                           title='Sửa thông tin danh bạ')
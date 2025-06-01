from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User, ALLOWED_ADMINS

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in ALLOWED_ADMINS and ALLOWED_ADMINS[username] == password:
            session['admin'] = username
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return render_template('auth/admin_login.html', error='Invalid admin credentials')

    return render_template('auth/admin_login.html')

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin.admin_login'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users, admin=session['admin'])

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin.admin_login'))

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin.admin_login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('admin.admin_login'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        gender = request.form['gender']

        if not username or not email or not phone or not city or not gender:
            return render_template('edit_user.html', user=user, error="All fields are required.")

        existing_user_email = User.query.filter(User.email == email, User.id != user_id).first()
        existing_user_username = User.query.filter(User.username == username, User.id != user_id).first()

        if existing_user_email:
            return render_template('edit_user.html', user=user, error="Email already in use.")
        if existing_user_username:
            return render_template('edit_user.html', user=user, error="Username already in use.")

        user.username = username
        user.email = email
        user.phone = phone
        user.city = city
        user.gender = gender

        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_user.html', user=user)

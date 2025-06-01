from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('auth/signup.html', error='Passwords do not match')
        
        if not phone.isdigit() or len(phone) != 10:
            return render_template('auth/signup.html', error='Phone number must be exactly 10 digits')

        if User.query.filter_by(username=username).first():
            return render_template('auth/signup.html', error='Username already taken')

        if User.query.filter_by(email=email).first():
            return render_template('auth/signup.html', error='Email already registered')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            username=username,
            email=email,
            phone=phone,
            city=city,
            gender=gender,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('auth/signup.html')

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            return redirect(url_for('dashboard.index'))
        else:
            flash("Hmm... those credentials don't match. Try again ❤️", category='error')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        display_name = request.form.get('display_name')

        if not username or not password or not confirm_password:
            flash('Required fields cannot be empty.', category='error')
        elif password != confirm_password:
            flash('Passwords must match.', category='error')
        elif User.query.filter_by(username=username).first():
            # In a real app we might want to hide that the user exists for security,
            # but usually for registration it is fine to say username is taken.
            flash('Username is already taken.', category='error')
        else:
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password, method='scrypt'),
                display_name=display_name
            )
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

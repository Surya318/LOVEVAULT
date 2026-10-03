from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('index.html')

@dashboard.route('/dashboard')
@login_required
def index():
    return render_template('dashboard.html', user=current_user)

@dashboard.route('/love-world')
@login_required
def love_world():
    return render_template('love_world.html', user=current_user)

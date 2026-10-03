from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Memory, ImportantDate, LoveLetter, TimelineEvent, Proposal, Surprise
from app import db
from datetime import datetime

features = Blueprint('features', __name__)

import os
from werkzeug.utils import secure_filename
from flask import current_app

@features.route('/memories', methods=['GET', 'POST'])
@login_required
def memories():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Ensure filename is unique or just save it
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_path = filename
        
        if title:
            new_memory = Memory(
                user_id=current_user.id,
                title=title,
                description=description,
                image_path=image_path,
                memory_date=datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
            )
            db.session.add(new_memory)
            db.session.commit()
            flash('Memory added successfully ❤️', 'success')
            return redirect(url_for('features.memories'))
            
    user_memories = Memory.query.filter_by(user_id=current_user.id).order_by(Memory.memory_date.desc()).all()
    return render_template('memories.html', memories=user_memories)

@features.route('/dates', methods=['GET', 'POST'])
@login_required
def dates():
    if request.method == 'POST':
        title = request.form.get('title')
        date_str = request.form.get('date')
        date_type = request.form.get('date_type')
        
        if title and date_str:
            new_date = ImportantDate(
                user_id=current_user.id,
                title=title,
                date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                date_type=date_type
            )
            db.session.add(new_date)
            db.session.commit()
            flash('Date added successfully 📅', 'success')
            return redirect(url_for('features.dates'))
            
    user_dates = ImportantDate.query.filter_by(user_id=current_user.id).order_by(ImportantDate.date.desc()).all()
    return render_template('dates.html', dates=user_dates)

@features.route('/letters', methods=['GET', 'POST'])
@login_required
def letters():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title and content:
            new_letter = LoveLetter(
                user_id=current_user.id,
                title=title,
                content=content
            )
            db.session.add(new_letter)
            db.session.commit()
            flash('Your love letter has been saved 💌', 'success')
            return redirect(url_for('features.letters'))
            
    user_letters = LoveLetter.query.filter_by(user_id=current_user.id).order_by(LoveLetter.created_at.desc()).all()
    return render_template('letters.html', letters=user_letters)

@features.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        
        if title and date_str:
            new_event = TimelineEvent(
                user_id=current_user.id,
                title=title,
                description=description,
                event_date=datetime.strptime(date_str, '%Y-%m-%d').date()
            )
            db.session.add(new_event)
            db.session.commit()
            flash('Timeline event added! 🧭', 'success')
            return redirect(url_for('features.timeline'))
            
    events = TimelineEvent.query.filter_by(user_id=current_user.id).order_by(TimelineEvent.event_date.asc()).all()
    return render_template('timeline.html', events=events)

@features.route('/proposal', methods=['GET'])
@login_required
def proposal():
    return render_template('proposal.html')

@features.route('/surprises', methods=['GET', 'POST'])
@login_required
def surprises():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        unlock_keyword = request.form.get('unlock_keyword')
        
        if title and unlock_keyword:
            new_surprise = Surprise(
                user_id=current_user.id,
                title=title,
                message=message,
                unlock_keyword=unlock_keyword
            )
            db.session.add(new_surprise)
            db.session.commit()
            flash('Secret surprise locked away! 🔒', 'success')
            return redirect(url_for('features.surprises'))
            
    all_surprises = Surprise.query.filter_by(user_id=current_user.id).order_by(Surprise.created_at.desc()).all()
    return render_template('surprises.html', surprises=all_surprises)

@features.route('/surprises/delete/<int:id>', methods=['POST'])
@login_required
def delete_surprise(id):
    surprise = Surprise.query.get_or_404(id)
    if surprise.user_id == current_user.id:
        db.session.delete(surprise)
        db.session.commit()
        flash('Surprise deleted.', 'success')
    return redirect(url_for('features.surprises'))

@features.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Add logic to change passcode later
        flash('Settings updated successfully! ✨', 'success')
        return redirect(url_for('features.settings'))
        
    return render_template('settings.html', user=current_user)

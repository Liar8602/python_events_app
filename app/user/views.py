from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from flask_mail import Mail, Message

import sqlite3
from ..email import sender
from ..config import DB_PATH
from app.models import db
from app.user.forms import LoginForm, RegistrationForm
from app.user.models import User, UserEvents
from app.event.models import Event

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('event.index'))
    title = 'Authorization'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You are going to the site')
            return redirect(url_for('event.index'))
    flash('Incorrect username or password')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('You have successfully left your personal page')
    return redirect(url_for('event.index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('event.index'))
    form = RegistrationForm()
    title = 'Registration'
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                        last_name=form.last_name.data, gender=form.gender.data, birthday=form.birthday.data,
                        role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your registration success')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}')
        return redirect(url_for('user.register'))


@blueprint.route('/subscribed')
def subscription():
    try:
        user_sub_events_id = [x.event_id for x in UserEvents.query.filter(UserEvents.user_id == current_user.id).all()]
        events = Event.query.filter(Event.id.in_(user_sub_events_id)).all()
        return render_template('event/index.html', events=events, user_events=user_sub_events_id)
    except:
        title = 'Where to go and what to do in Ufa'
        events = Event.query.order_by(Event.date_start).all()
        flash('You are not subscribed to more than one event. Subscribe!')
        return render_template('event/index.html', page_title=title, events=events)


@blueprint.route('/reset_password', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        conn = sqlite3.connect(r"C:\projects\final\flask_events_app\flask_events_app\app.db")
        forgotten_email = request.form["forgetpass"]
        all_emails = conn.execute('SELECT email FROM user where email = ?', (forgotten_email,))
        if all_emails.fetchone()[0] != None:
            needed_id = conn.execute('SELECT id FROM User where email = ?', (forgotten_email,))
            forgotten_password = conn.execute(
                "SELECT password FROM user WHERE id = %d" % (needed_id.fetchone()[0]))
            sender(forgotten_password, forgotten_email)
            flash('The instructions have been sent to your email address')
            return redirect(url_for('event.index'))
        else:
            flash("You may have entered an incorrect email address")
            return redirect(url_for('user.login'))
    else:
        return render_template('user/reset_password.html')

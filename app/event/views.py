from flask import abort, Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import or_
from app.event.models import Comment, Event
from app.event.forms import CommentForm, SearchForm
from app.user.models import UserEvents
from app.models import Category, db
from connect_db import get_data_from_db_by_search

blueprint = Blueprint('event', __name__)


@blueprint.route('/')
def index():
    title = 'Where to go and what to do in Ufa'
    events = Event.query.order_by(Event.date_start).all()
    return render_template('event/index.html', page_title=title, events=events)


@blueprint.route('/category/<category_id>')
def event_by_category(category_id):
    category_events = Event.query.filter(Event.category_id == category_id).order_by(Event.date_start).all()
    user_sub_events_id = [x.event_id for x in UserEvents.query.filter(UserEvents.user_id == current_user.id).all()]
    return render_template('event/index.html', events=category_events, user_events=user_sub_events_id)


@blueprint.route('/event/comment', methods=['POST'])
@login_required
def add_comment(event_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.text.data,
            event_id=event_id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added success')
        return redirect('event.index')


@blueprint.route('/event/<int:event_id>')
def single_event(event_id):
    my_event = Event.query.filter(Event.id == event_id).first()
    form = CommentForm()
    if not my_event:
        abort(404)
    return render_template('event/single_event.html', event=my_event, comment_form=form)


@blueprint.route('/subscribe/<int:event_id>/')
def subscribe_event(event_id):
    is_user_subscribed = UserEvents.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if is_user_subscribed:
        return redirect(url_for('event.index'))
    else:
        current_user.subscribe(event_id=event_id)
        return redirect(url_for('event.index'))


@blueprint.route('/unsubscribe/<int:event_id>')
def unsubscribe_event(event_id):
    is_user_unsubscribed = UserEvents.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if is_user_unsubscribed:
        current_user.unsubscribe(event_id=event_id)
        return redirect(url_for('event.index'))
    else:
        return redirect(url_for('event.index'))


@blueprint.route('/search', methods=['GET'])
def search_results(search):
    search = SearchForm()
    search_str = f"%{search.search.data}%"
    if search.validate_on_submit():
        search_result_data = get_data_from_db_by_search(search_str)
        return render_template('event/search_results.html', event=search_result_data, search_str=search_str)
    else:
        flash(f'Nothing was found in the search results for {search_str}')
        return redirect(url_for('event.index'))

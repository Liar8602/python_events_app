from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db

Model = db.Model
Column = db.Column
ForeignKey = db.ForeignKey
relationship = db.relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Enum('male', 'female', name='gender'))
    birthday = db.Column(db.Date, nullable=True)
    is_active = Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.String(10), index=True)
    subscribed_events = relationship('UserEvents', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_subscribe(self, event_id):
        sub = UserEvents(user_id=self.id, event_id=event_id)
        db.session.add(sub)
        db.session.commit()

    def unsubscribe(self, event_id):
        sub = UserEvents.query.filter_by(user_id=self.id, event_id=event_id).first()
        db.session.delete(sub)
        db.session.commit()

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'User name={self.username, self.id}'


class UserEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), index=True)
    user = db.relationship('User', back_populates='events')
    event = db.relationship('Event', back_populates='users')

    def __repr__(self):
        return f'Subscribe={self.id}'

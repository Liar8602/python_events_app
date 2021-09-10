from app.models import db
import datetime


class Event(db.Model):
    __searchable__ = ['title', 'description']
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), unique=True, nullable=False)
    date_start = db.Column(db.Date, nullable=True)
    date_finish = db.Column(db.Date, nullable=True)
    description = db.Column(db.String(150), nullable=True)
    place = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    price = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category_id'))
    category = db.relationship('Category', backref='events')
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource', backref='events')

    def comments_count(self):
        return Comment.query.filter(Comment.event_id == self.id).count()

    def __repr__(self):
        return f'<Events {self.title} {self.url}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id', ondelete='CASCADE'),
        index=True
    )
    event = db.relationship('Event', backref='comments')
    user = db.relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comments {self.id}>'

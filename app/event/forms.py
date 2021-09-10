from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.event.models import Event


class CommentForm(FlaskForm):
    event_id = HiddenField('ID event', validators=[DataRequired()])
    comment_text = StringField('Comments', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Send', render_kw={'class': 'btn btn-primary'})

    def validates_event_id(self, event_id):
        if not Event.query.get(event_id.data):
            raise ValidationError('You are trying to comment on an event with a non-existent id')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-secondary border-0'})

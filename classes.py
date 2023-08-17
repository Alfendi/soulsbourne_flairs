from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length
import praw


class LoginManager:
    def __init__(self) -> None:
        self.verified = False

    def get_state(self):
        return self.verified

    def set_verified(self):
        self.verified = True


class Verification(FlaskForm):
    passkey = StringField('passkey', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Submit')


class GameChoices(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FlairChange(FlaskForm):
    games = [('DeS', 'Demon\'s Souls'), ('DaS', 'Dark Souls'), ('DaS2', 'Dark Souls 2'), ('Bb', 'Bloodborne'),
             ('DaS3', 'Dark Souls 3'), ('Sek', 'Sekiro'), ('Eld', 'Elden Ring')]

    name = StringField('name', validators=[DataRequired(), Length(min=1, max=20)])
    flairs = GameChoices(u'Subreddit Flairs', choices=games)
    submit = SubmitField('Submit')

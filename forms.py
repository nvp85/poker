from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class CardForm(FlaskForm):
    suit = SelectField("suit", choices=[('club', 'club'), ('spade', 'spade'), ('diamond', 'diamond'), ('heart', 'heart')])
    rank = SelectField("rank", choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('J', 'Jack'), ('Q', 'Queen'), ('K', 'King'), ('A', 'Ace')])

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MyForm(FlaskForm):
    name = StringField('Prénom', id='name', validators=[DataRequired(), Length(max=50)])
    lastname = StringField('Nom', id='lastname', validators=[DataRequired(), Length(max=50)])
    login = StringField('Login', id='login', validators=[DataRequired(), Length(max=30)])
    desc = TextAreaField('Description', id='desc', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Ajouter')


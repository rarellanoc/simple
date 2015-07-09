from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class MyForm(Form):
    name = StringField('name', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])
    password = PasswordField('password', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])
    ciudad = StringField('ciudad', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])

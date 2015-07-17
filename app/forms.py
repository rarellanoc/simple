from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField  
from wtforms.validators import DataRequired, Length, Email, EqualTo

class MyForm(Form):
    mail = EmailField('correo', validators=[DataRequired(),Length(min=5, max=20, message="direccion fuera de rango"),Email("Ingrese un correo real")])
    password = PasswordField('password', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])

    
class MyFormulario(Form):
    Telefono = StringField('Telefono', validators=[DataRequired(),Length(min=5, max=20, message="telefono fuera de rango")])
    Correo = PasswordField('Correo', validators=[DataRequired(),Length(min=5, max=20, message="direccion fuera de rango")])
    Direccion = StringField('Direccion', validators=[DataRequired(),Length(min=5, max=20, message="direccion fuera de rango")])

	
	
class RegistroForm(Form):
    mail = EmailField('correo', validators=[DataRequired(),Length(min=5, max=20, message="direccion fuera de rango"), Email("Ingrese un correo real")])

    token = StringField('token', validators=[DataRequired(),Length(min=6, max=7, message="token no valido")])



    password = PasswordField('password', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango"), EqualTo('password_r', message='Passwords deben coincidir')])
    password_r = PasswordField('password rep', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])

    
class LoginForm(Form):
    email = EmailField('correo', validators=[DataRequired(),Length(min=5, max=20, message="direccion fuera de rango"),Email("Ingrese un correo real")])
    password = PasswordField('password', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])
	
class TokenForm(Form):
    email = EmailField('correo', validators=[DataRequired(),Length(min=5, max=20, message="direccion fuera de rango"), Email("Ingrese un correo real")])
    


	
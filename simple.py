from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from flask_mail import Mail, Message
from flask_weasyprint import HTML, render_pdf


from flask.ext.sqlalchemy import SQLAlchemy




import config


app = Flask(__name__)

db = SQLAlchemy(app)


import model



app.config.from_object('config')

mail = Mail(app)


app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass

class MyForm(Form):
    name = StringField('name', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])
    password = PasswordField('password', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])
    ciudad = StringField('ciudad', validators=[DataRequired(),Length(min=5, max=20, message="nombre fuera de rango")])
# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin


class User(UserMixin):
    '''Simple User class'''
    USERS = {
        # username: password
        'john': 'love mary',
        'mary': 'love peter'
    }

    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None


# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.get(id)


@app.route('/')
def index():  
    
    if current_user.is_authenticated():
        
        return redirect(url_for('home'))
        
        
    return render_template('landing.html')
        
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/success')
def success(name):
    return render_template('success.html', name=name)


@app.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
    user = User.get(request.form['username'])
    if (user and user.password == request.form['password']):
        login_user(user)
        
    else:
        flash('Usuario o clave incorrecta')

    return redirect(url_for('index'))


@app.route("/sendmail")
def sendmail():

    	msg = Message("Hello",
                  sender="madeer.lab@gmail.com",
                  recipients=["its.arellano@gmail.com"])

@app.route('/formulario', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
       return success(request.form['name'])
	# return redirect(url_for('/success', name=form.name))
    return render_template('formulario.html', form=form)

	msg.body = "testing"
	msg.html = "<b>testing</b>"

	mail.send(msg)

	return "Enviado"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/hello_<name>.pdf')
def hello_pdf(name):
    # Make a PDF straight from HTML in a string.
    html = render_template('hello.html', name=name)
    return render_pdf(HTML(string=html))



@app.route('/home')
@login_required
def home():
    return render_template('home.html')
    





@app.route("/coleccion")
def holaColeccion():
        nombrevalue = "Ricardo"
        return render_template('coleccion.html', nombre=nombrevalue)

@app.route("/directorio")
def holaDirectorio():
        nombrevalue = "Ricardo"
        return render_template('directorio.html', nombre=nombrevalue)

@app.route("/estadisticas")
def holaEstadisticas():
        nombrevalue = "Ricardo"
        return render_template('estadisticas.html', nombre=nombrevalue)


if __name__ == "__main__":
    app.debug = True
    app.run()

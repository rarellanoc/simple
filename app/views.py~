from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

from flask_mail import Mail, Message
from flask_weasyprint import HTML, render_pdf



from app import app, model, forms, db

from forms import MyFormulario
from forms import MyForm
from model import User, usuarios



@app.route('/')
def index():  
    
    if current_user.is_authenticated():
        
        return redirect(url_for('home'))
        
        
    return render_template('landing.html')


login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass

@login_manager.user_loader
def load_user(id):
    return User.get(id)
        
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
    msg.body = "testing"
    msg.html = "<b>testing</b>"

    mail.send(msg)

    return "Enviado"

@app.route('/formulario', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
       return success(request.form['name'])
	# return redirect(url_for('/success', name=form.name))
    return render_template('formulario.html', form=form)

	


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/database')
def database():
    
	me = usuarios('admin', 'hola-2015')
	db.session.add(me)
	db.session.commit()


    	return render_template('database.html')


@app.route('/hello_<name>.pdf')
def hello_pdf(name):
    
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


@app.route("/select_<username>")
def select(username):
	tododeluser = usuarios.query.filter_by(user=username).first_or_404()
	
	encontrado = 'si'

	return render_template('select.html' , usuario = tododeluser.user , ok=encontrado) 	

@app.route("/solicitudes")
def holaSolicitudes():
        return render_template('solicitudes.html')

@app.route("/conocer")
def holaConocer():
        return render_template('conocer.html')

@app.route('/perfil', methods=('GET', 'POST'))
def datos():
    form = MyFormulario()
    if form.validate_on_submit():
       return success(request.form['name'])
	# return redirect(url_for('/success', name=form.name))
    return render_template('perfil.html', form=form)


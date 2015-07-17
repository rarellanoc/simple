import time, os, types

from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template, g, jsonify
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask.ext.restful import reqparse, abort, Api, Resource
from flask_mail import Mail, Message
#from flask_weasyprint import HTML, render_pdf

from flask.ext.sqlalchemy import SQLAlchemy

from json import dumps

import json

from app import app, model, forms, db

from forms import MyFormulario
from forms import MyForm, RegistroForm, LoginForm
from model import *



api = Api(app)


@app.route('/')
def index():  
    
    if current_user.is_authenticated():
        
        solicitudes = Solicitud.query.filter_by(id_user=current_user.id)

        nro_solic = solicitudes.count()
        
        return render_template('home.html', nro = nro_solic)
        
        
    return render_template('landing.html')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


#@app.route('/login')
#def login():
#    form = MyForm()
#    
#    
#    if form.validate_on_submit():
#        return redirect(url_for('login_check'))
#    return render_template('login.html', form=form)

@app.route('/success')
def success(name):
    return render_template('success.html', name=name)


@app.route('/login', methods=('GET', 'POST'))
def login_check():
    # validate username and password
    
    form = LoginForm()
    
    if form.validate_on_submit():
        
        email = request.form['email']

        registered_user = User.query.filter_by(email=email).first()

        if registered_user is None:

            return redirect(url_for('index'))

        else:

            pw = request.form['password']	
            if (registered_user.check_password(pw)):
                login_user(registered_user)

            else:
                flash('Usuario o clave incorrecta')

        
        return redirect(url_for('index'))
    
    
    return render_template('login.html', form=form)


def sendmail(quien):

    msg = Message("Hello",
                  sender="madeer.lab@gmail.com",
                  recipients=[quien])
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


@app.route('/registro', methods=('GET', 'POST'))
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
		
        if request.method == 'POST' and form.validate():

            mail = form.mail.data
            passs = form.password.data
            token = form.token.data
            
            if Token.query.filter_by(token=token, disponible="si").first() != None:
                

                user = User(email=mail,password=passs)
                #sendmail(str(user.correo))

                t = Token.query.filter_by(token=token).first()
                t.disponible = "no"
                db.session.commit()

                db.session.add(user)

                idfortest = User.query.filter_by(email=mail).first()

                testdata(idfortest)

                db.session.commit()

                #flash('Gracias por registrarse, recibira un correo de confirmacion')
                return render_template('confirmar.html', user=user)
            
            else:
                flash('token no valido')
                return render_template('registro.html', form=form)
    return render_template('registro.html', form=form)



@app.route('/tokenadd_<token>')
@login_required
def add_tokens(token):
    
    t = Token(token=token)
    db.session.add(t)
    db.session.commit()
    
    return "token added"


def testdata(user):


    #usuario = User(email='elarellano@gmail.com',password='holachao123')
    #db.session.add(usuario)

    solicitud1 = Solicitud(titulo='hola, esta es una solicitud', cuerpo='madeer desea que compartas este sitio con dise&ntilde;adores', id_user=user.id)
    db.session.add(solicitud1)
    solicitud2 = Solicitud(titulo='puedes eliminarlas en cualquier momento', cuerpo='gracias por registrarte, esta es una solicitud de prueba, peudes eliminarla', id_user=user.id)
    db.session.add(solicitud2)
    solicitud3 = Solicitud(titulo='madeer te pide que visites su blog', cuerpo='vista el blog', id_user=user.id)
    db.session.add(solicitud3)
    
    
    



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#@app.route('/database')
#def database():
    
#	me = usuarios('admin', 'hola-2015')
#	db.session.add(me)
#	db.session.commit()


 #   	return render_template('database.html')


#@app.route('/hello_<name>.pdf')
#def hello_pdf(name):
    
#   html = render_template('hello.html', name=name)
#    return render_pdf(HTML(string=html))


@app.route('/confirmar')
def confirmar():
    return render_template('home.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')
    

@app.route("/coleccion")
def holaColeccion():

    htmlpage = 'coleccion.html'
    return default(htmlpage)
@app.route("/directorio")
def holaDirectorio():
    
    htmlpage = 'directorio.html'
    return default(htmlpage)

@app.route("/estadisticas")
def holaEstadisticas():

    htmlpage = 'estadisticas.html'
    return default(htmlpage)

    
    

def default(htmlpage):
    

    nro_solic = 0

    if current_user.is_authenticated():

        solicitudes = Solicitud.query.filter_by(id_user=current_user.id)

        nro_solic = solicitudes.count()
    return render_template(htmlpage, nro = nro_solic)


#@app.route("/select_<username>")
#def select(username):
#	tododeluser = usuarios.query.filter_by(user=username).first_or_404()
#	
#	encontrado = 'si'
#
#	return render_template('select.html' , usuario = tododeluser.user , ok=encontrado) 	

@app.route("/solicitudes")
@login_required
def holaSolicitudes():
    solicitudes = Solicitud.query.filter_by(id_user=current_user.id)
    
    nro = solicitudes.count()
    return render_template('solicitudes.html', solicitudes = solicitudes, nro = nro)

@app.route("/conocer")
def holaConocer():
        return render_template('conocer.html')

@app.route("/mensaje")
def holaMensaje():
        return render_template('mensaje.html')

@app.route('/perfil', methods=('GET', 'POST'))
def datos():
    form = MyFormulario()
    if form.validate_on_submit():
        return success(request.form['name'])
	# return redirect(url_for('/success', name=form.name))
    return render_template('perfil.html', form=form)



@app.route('/users', methods=['GET'])
def get_all_users():
	# get query parameters
	offset = request.args.get('offset')
	limit  = request.args.get('limit')
	# query database using SQLAlchemy
	users = User.query.offset(offset).limit(limit).all()
	# return object
	return wrapper( users )

@app.route('/users', methods=['POST'])
def create_user():
	# create User object from JSON data	
 
    if request.json == None:
        print "json none"
    else:
        print "json ok"
            
            
	user = User(json=request.json)

	# save to DB
	#db.session.begin()
	try:
		db.session.add(user)
		db.session.commit()
	except:
		db.session.rollback()
		
	# return formated and sorted JSON object
    
	return json.dumps("registro completo")


# Wrapper object which returns JSON total number of objects plus array of objects
#
def wrapper(data):

	if data == None:
		abort(404)
		
	output = None
	if isinstance(data, types.ListType):
		output = []
		for obj in data:
			output.append(obj.to_dict())
	else:
		output = (data.to_dict())
		
	return jsonify(total = len(output), data=output)


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()

parser.add_argument('task', type=str)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# Todo
#   show a single todo item and lets you delete them
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


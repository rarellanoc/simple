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
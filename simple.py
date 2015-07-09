from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass


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


@app.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
    user = User.get(request.form['username'])
    if (user and user.password == request.form['password']):
        login_user(user)
        
    else:
        flash('Usuario o clave incorrecta')

    return redirect(url_for('index'))






@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




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

@app.route("/perfil")
def holaPerfil():
        nombrevalue = "Ricardo"
        return render_template('perfil.html', nombre=nombrevalue)


if __name__ == "__main__":
    app.debug = True
    app.run()

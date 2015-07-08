
from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)

@app.route("/")
def hola():
	nombrevalue = "Ricardo"
	return render_template('home.html', nombre=nombrevalue)

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

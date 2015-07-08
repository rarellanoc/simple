from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)

@app.route("/")
def hola():
	nombrevalue = "Ricardo"
	return render_template('home.html', nombre=nombrevalue)

if __name__ == "__main__":
    app.debug = True
    app.run()

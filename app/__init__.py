
import os
from config import basedir

from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from flask_mail import Mail, Message
from flask_weasyprint import HTML, render_pdf


from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


import config





db = SQLAlchemy(app)



app.config.from_object('config')

mail = Mail(app)



from app import forms
    



import views
import model
from model import User

if __name__== '__main__':
    app.run(debug=True)
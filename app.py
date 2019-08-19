import os
from functools import update_wrapper

from flask import Flask, render_template, redirect, url_for, request, session, g
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, current_user, login_user
from flask_session import Session
from flaskext.mysql import MySQL
import time, datetime

from werkzeug.urls import url_parse

from Modelo import User

from werkzeug.utils import secure_filename, escape

from templates import web_services, auth, admin

app = Flask(__name__)
# my sql connection
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1390'
app.config['MYSQL_DATABASE_DB'] = 'vinos_final'

UPLOAD_FOLDER = 'c:/ni_idea'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mysql = MySQL(app)

app.secret_key = 'clve'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

#app.register_blueprint(usuario.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(web_services.bp)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)


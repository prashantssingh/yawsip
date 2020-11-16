from flask import request, render_template, flash, redirect, make_response, g
from app import app
import logging

from werkzeug.utils import secure_filename

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

import os

# MySQL connection params
HOSTNAME='localhost'
DATABASE='yawsip'
USERNAME='root'
PASSWORD='prash94@MySQL'

app.config['UPLOAD_FOLDER'] = "./upload-folder"
app.secret_key = os.urandom(24)

def get_db_connection():
    return mysql.connector.connect(
                host=HOSTNAME,
                database=DATABASE,
                user=USERNAME,
                password=PASSWORD
            )

def get_db_cursor(db_connection):
    return db_connection.cursor()

@app.route('/')
@app.route('/home')
def index():
    return render_template('dashboard.html')


@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign-up.html')

    mandatory_fields = ["firstname", "lastname", "username", "password", "groupnames"]
    if not all(field in request.form for field in mandatory_fields):
        app.logger.error(f'path: /signup, mandatory field(s) missing. data received in request: {request.form}')
        return redirect('/home')
    app.logger.debug(f'path: /user/signup, data received in request: {request.form}')
    
    db_connection = get_db_connection()
    db_cursor = get_db_cursor(db_connection)
    

    query = 'INSERT INTO user (fname, lname, username, password, groupnames) values (%s, %s, %s, %s, %s)'
    data = (request.form['firstname'],request.form['lastname'], request.form['username'], request.form['password'], request.form['groupnames'])
    
    try:
        db_cursor.execute(query, data)
        db_connection.commit()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    return redirect('/user/login')


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    mandatory_fields = ["username", "password"]
    if not all(field in request.form for field in mandatory_fields):
        app.logger.error(f'path: /login, mandatory field(s) missing. data received in request: {request.form}')
        return redirect('/home')
    app.logger.debug(f'path: /user/login, data received in request: {request.form}')

    db_connection = get_db_connection()
    db_cursor = get_db_cursor(db_connection)
    
    record = None
    try:
        db_cursor.execute("SELECT password from user WHERE username = %s", (request.form["username"],))
        record = db_cursor.fetchone()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    if not record:
        app.logger.debug("path: /user/login, invalid Username or password")
        flash('Invalid Username or password')
        return redirect('/user/login')
    else:
        app.logger.debug(f'path: /user/login, user fetched from db: {record}')
        # flash('You were successfully logged in') 

    if record[0] != request.form["password"]:
        flash('Invalid Username or password')
        return redirect('/user/login')

    return redirect('/home')


@app.route('/upload', methods = ['POST'])
def upload_file():
    if "file" not in request.files:
        return "No user_file key in request.files"

    file = request.files['file']
    file.save(secure_filename(file.filename))
    return 'file uploaded successfully'

@app.errorhandler(404)
def not_found(some):
    """Page not found."""
    return render_template("404.html")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

if __name__ == '__main__':
   app.run(debug = True)
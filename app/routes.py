from flask import request, render_template, flash, redirect, make_response, g, session
from flask_mail import Mail, Message
from app import app
import logging
import os

from werkzeug.utils import secure_filename

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

import os

HOST_URL = "http://localhost:5000/"

# MySQL connection params
HOSTNAME='localhost'
DATABASE='yawsip'
# USERNAME='pxs3374_app_user'
USERNAME='root'
PASSWORD='prash94@MySQL'
# PASSWORD='Hello94@World'

# Mail configurations
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cse5382mail@gmail.com'
app.config['MAIL_PASSWORD'] = 'Hello5382@world'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['UPLOAD_FOLDER'] = upload_folder = "./upload-folder"
app.secret_key = os.urandom(24)

current_user = ""
data = []

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

    mandatory_fields = ["firstname", "lastname", "email", "username", "password", "groupnames"]
    if not all(field in request.form for field in mandatory_fields):
        app.logger.error(f'path: /signup, mandatory field(s) missing. data received in request: {request.form}')
        return redirect('/home')
    app.logger.debug(f'path: /user/signup, data received in request: {request.form}')
    
    query = 'INSERT INTO user (fname, lname, email, username, password, groupnames) values (%s, %s, %s, %s, %s, %s)'
    data = (request.form['firstname'], request.form['lastname'], request.form['email'], request.form['username'], request.form['password'], request.form['groupnames'])
    execute_query(query, data)
    
    groups = request.form['groupnames'].split()
    query = 'INSERT INTO user_group (username, groupname) values (%s, %s)'
    for group in groups:
        execute_query(query, (request.form['username'], group))
        
    # send mail..
    mail_body = r"""
Hi $$NAME$$,

Thank you for signing up with YAWSIP. One last step in the process is to verify your email. Please follow below link to activate your account with us:
$$LINK$$

Please contact us at cse5382mail@gmail.com for queries.

Thank you 
--
Regards,
YAWSIP Team
"""
    msg = Message('Hello', sender = 'cse5382mail@gmail.com', recipients = [request.form['email']])
    mail_body = mail_body.replace("$$NAME$$", request.form['firstname'])
    mail_body = mail_body.replace("$$LINK$$", f"{HOST_URL}/user/verifyaccount/{request.form['username']}")
    msg.body = mail_body
    mail.send(msg)

    return redirect('/user/login')


@app.route('/user/verifyaccount/<username>', methods=['GET'])
def verify_account(username):
    query = f'UPDATE user SET status = "Verified" WHERE username = "{username}"'
    execute_query(query, None)
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
        db_cursor.execute("SELECT password, status from user WHERE username = %s", (request.form["username"],))
        record = db_cursor.fetchone()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    if not record:
        app.logger.debug("path: /user/login, invalid Username or password")
        flash('Invalid Username: No such user found')
        return redirect('/user/login')

    app.logger.debug(f'path: /user/login, user fetched from db: {record}')
    if record[1] != "Approved":
        flash('Admin is yet to approve your account')
        return redirect('/home')

    if record[0] != request.form["password"]:
        flash('Invalid password, please try again')
        return redirect('/user/login')

    session['logged_in'] = True

    global current_user
    current_user = request.form["username"]
    return redirect('/home')


@app.route("/admin/getallusers", methods = ['GET'])
def getallusers():
    global data
    db_connection = get_db_connection()
    db_cursor = get_db_cursor(db_connection)
    
    records = []
    try:
        db_cursor.execute("SELECT fname, lname, groupnames FROM user WHERE status = 'Verified';")
        records = db_cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    if not records:
        app.logger.debug("path: /admin/getallusers, no users left to authenticate")
        flash('No users left to authenticate')
        return render_template('dashboard.html')

    global data
    data = records
    app.logger.debug(f'path: /admin/getallusers, user fetched from db: {records}')
    return redirect('/home')


@app.route("/admin/approveuser/<username>", methods = ['GET'])
def approve_user(username):
    query = f'UPDATE user SET status = "Approved" WHERE username = "{username}"'
    execute_query(query, None)
    return redirect('/home')


@app.route("/user/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html') 


@app.route('/user/upload', methods = ['POST'])
def upload_file():
    app.logger.debug(f'path: /user/upload, Files in req dict: {request.files}')
    mandatory_params = ["username", "groupname"]
    if not all(param in request.args for param in mandatory_params):
        app.logger.error(f'path: /user/upload, mandatory field(s) missing. args received in request: {request.args}')
        return render_template('dashboard.html')

    if "file" not in request.files:
        app.logger.debug('path: /user/upload, No file key in request.files')
        return render_template('dashboard.html')

    file = request.files['file']
    file.save(os.path.join(upload_folder, secure_filename(file.filename)))

    # insert into database
    query = f'INSERT INTO upload (username, filename, groupname) Values (%s, %s, %s)'
    execute_query(query, (request.args['username'], file.filename, request.args['groupname']))

    app.logger.debug('path: /user/upload, file uploaded successfully')
    return render_template('dashboard.html')


@app.errorhandler(404)
def not_found(some):
    """Page not found."""
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(some):
    """Interval Server Error."""
    return render_template("500.html")

def execute_query(query, data):
    db_connection = get_db_connection()
    db_cursor = get_db_cursor(db_connection)

    try:
        if data: 
            db_cursor.execute(query, data)
        else:
            db_cursor.execute(query)

        db_connection.commit()
    except mysql.connector.Error as error:
        raise f"Failed to update user, err: {error}"


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
   app.run(debug = True)
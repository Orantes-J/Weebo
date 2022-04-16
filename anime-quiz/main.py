import email
from email.policy import default
from hashlib import new
import os
from tkinter import CURRENT
from flask import Flask, render_template, redirect, url_for, request, session
from flask.helpers import flash
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from flask import send_from_directory
import random
from flask_login import LoginManager
from flask_login import login_user
from flask_session import Session
# MODULES 
import news

# SECURING ROUTES
from email import utils
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


auth = HTTPBasicAuth()
user = 'juan.carlos@email.com'
pw = '1234xyz'

users = {
    user : generate_password_hash(pw)
}

session_info = []

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

# READING ANIME QUESTIONS
import csv
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import InputRequired
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'DUMMYpassword'
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# CREATING SESSION
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

def print_state(str):
    print("*"*50)
    print(f"{str}")
    print("*"*50)

@login_manager.user_loader
def load_user(user_id):
    user = []
    mycursor.execute(f"SELECT id FROM user_example WHERE id ={user_id}")
    only_user = mycursor.fetchall()
    for i in only_user:
        user.append(i)
    return user
# ---------------------------------DATABASE FORMS---------------------------------

class Review(FlaskForm):
    name = StringField(label="Name", validators=[InputRequired()])
    rating = IntegerField(label="Rating (e.g 1-10)",  validators=[InputRequired()])
    user_review = TextAreaField(label= "Review", validators=[InputRequired()])

# ---------------------------------CONNECT DATABASE---------------------------------

weeb_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='weeb_db'
)
mycursor = weeb_db.cursor()
mycursor.execute('SHOW TABLES')

db_tables = mycursor.fetchall() #this method grabs all tables. Without it, it will return a NONE TYPE OBJECT 
# print('*'*50)
# print(db_tables)
# print('*'*50)
# ----------------------------------------------------------------------------------

# ---------------------------------CONNECT DATABASE---------------------------------

weeb_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='weeb_db'
)
mycursor = weeb_db.cursor()
mycursor.execute('SHOW TABLES')
db_tables = mycursor.fetchall() #this method grabs all tables. Without it, it will return a NONE TYPE OBJECT 
# print('*'*50)
# print(db_tables)
# print('*'*50)

# ----------------------------------------------------------------------------------
correct = "✔"
incorrect = "⛔"
question_iteration = 1
answer_stats = []
anime_quizes = []
mycursor.execute("SELECT * FROM anime_quizzes")
my_quizzes = mycursor.fetchall()
for a in my_quizzes:
    anime_quizes.append(a)

# --------------------------------- MODULE CODE -> FUNCTION CALLS ---------------------------------
list_of_users = []
email_carlos = 'carlos@email.com'
user_name = "carlos orantes"
user_password = "1235"
user_username = "showboy"
mycursor.execute(f"SELECT email FROM user_example WHERE email = '{email_carlos}'")
fetched_emails = mycursor.fetchall()
for i in fetched_emails:
    list_of_users.append(i)
# news.create_users(list_of_users, email=email_carlos, name=user_name, password=user_password, username=user_username)
# -------------------------------------------------------------------------------------------------

# GETTING QUIZZES FROM DB 
question_num = 0

def reset_quiz():
    global answer_stats
    global question_num
    answer_stats = []
    question_num = 0

@app.route('/')
def home():
    reset_quiz()
    reviews_list = []
    available_quizes = []
    art_submissions = []
    question_num = 0

    # REVEIWS
    mycursor.execute("SELECT * FROM alias_review")
    results = mycursor.fetchall()
    for i in results:
        reviews_list.append(i)
    # QUIZZES
    mycursor.execute("SELECT * FROM anime_quizzes")
    my_quizzes = mycursor.fetchall()
    for a in my_quizzes:
        available_quizes.append(a)
    # ART SUBMISSIONS
    mycursor.execute("SELECT * FROM art_submission")
    submissions = mycursor.fetchall()
    for b in submissions:
        art_submissions.append(b)

    # USER SESSION INFORMATION
    logged_user = []
    try:
        mycursor.execute(f'SELECT * FROM user_example WHERE id = {session["user_id"]}')
        fetch_logged = mycursor.fetchall()
        for i in fetch_logged:
            logged_user.append(i)
    except:
        pass

    context = {
        "user" : logged_user
    }

    return render_template('index.html', arts = art_submissions, lot=available_quizes, all_reviews = reviews_list, context=context)

@app.route('/anime-quiz', methods = ["GET", "POST"])
def quiz():
    global answer_stats
    list_of_choices = []

    # GETS PASSED IN ARGUMENTS IN URL AND IS USED TO GRAB CORRECT TXT FILE
    anime_id = request.args.get('id')
    id_num = int(anime_id)
    anime_name = request.args.get('name')
    anime_info = anime_quizes[int(anime_id) - 1]
    
    # READS AN ANIME FILE ACCORDING TO ANIME CHARACTER USED DYNAMIC STRAT 
    list_of_questions = []
    with open (anime_quizes[id_num-1][2], 'r') as anime:
        for i in anime:
            rr = csv.reader(anime)
            for a in rr:
                list_of_questions.append(a)

    
    # APPENDS SLICED LIST INTO NEW ARRAY WHICH ONLY CONTAIN ANSWERS 
    for a in list_of_questions:
        choices = a[2:]
        random.shuffle(choices)
        list_of_choices.append(choices)

    return render_template('quiz.html', stats= answer_stats, shuffled_list = list_of_choices, anime_info = anime_info, anime_it = int(anime_id), question_num = question_num, anime_questions = list_of_questions)

@app.route('/check_answer/<a>', methods=['GET', 'POST'])
def check_answer(a):
    global question_num
    answer = request.form.get('correct-answer')
    name = request.form.get('anime-name')
    id = request.form.get('anime-id')
    if request.method == "POST":
        user_answer = request.form['choices']
        if "".join(user_answer.split()) == "".join(answer.split()):
            question_num = question_num + 1
            answer_stats.append(correct)
        else:
            question_num = question_num + 1
            answer_stats.append(incorrect)
        return redirect(f'/anime-quiz?name={name}&id={id}')

@app.route('/anime-news')
def anime_news():
    reset_quiz()
    news_list = []
    mycursor.execute("SELECT * FROM anime_newss")
    results = mycursor.fetchall()
    for i in results:
        news_list.append(i)
    return render_template('anime-news.html', all_news = news_list)

@app.route('/all-quizes', methods=['GET', 'POST'])
def quizes():
    reset_quiz()
    review_form = Review()
    #----------------------- RETRIEVING ALIAS REVIEW DATA ---------------------------
    
    reviews_list = []
    mycursor.execute("SELECT * FROM alias_review")
    results = mycursor.fetchall()
    for i in results:
        reviews_list.append(i)

    # -------------------------------------------------------------------------------
    
    if request.method == "POST":
        # testing if prints client is able to pass in data
        recieved_name = request.form.get('name')
        recieved_rating = request.form.get('rating')
        recieved_review = request.form.get('user_review')

    # ------------------------INSERTING VALUES TO TABLE-----------TABLE: ALIAS_REVIEW

        sql_command = "INSERT INTO alias_review(name, rating, review) VALUES(%s, %s, %s)"
        sql_values = (recieved_name, recieved_rating, recieved_review)
        mycursor.execute(sql_command, sql_values)
        weeb_db.commit()
        # print('*'*50)
        # print(mycursor.rowcount, 'record inserted')
        # print('*'*50)

        #----------------------------------------------------------------------------
        return redirect(url_for('quizes'))
    return render_template('quizes.html', all_reviews = reviews_list ,all_quizes = anime_quizes, form = review_form)

# ------------------- UPLOAD USER SUBMISSION SETTING --------------------------------

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/art-submissions', methods = ["GET", "POST"])
def submissions():
    reset_quiz()
    art_submissions = []
    mycursor.execute("SELECT * FROM art_submission")
    submissions = mycursor.fetchall()
    for b in submissions:
        art_submissions.append(b)
    
    return render_template('art-submissions.html', arts = art_submissions)

@app.route('/Calei')
def idk():
    return render_template('first.html')

@app.route('/submit-art', methods = ["POST", "GET"])
def submit_art():
    if request.method == "POST":
        # CHECK IF THE POST REQUEST HAS THE FILE PART
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # if the user tries to bypass a submition, the browser submits an empty file without a filename.
        if file.name == "":
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # ADD TO DATABASE IMAGE URL, CAPTION, LINKS AND USER
            art_caption = request.form['caption']
            artist_name = request.form['name']
            artist_link = request.form['link']
            sql_command = "INSERT INTO art_submission(caption, name, link, image_path) VALUES(%s, %s, %s, %s)"
            sql_values = (art_caption, artist_name, artist_link, filename)
            mycursor.execute(sql_command, sql_values)
            weeb_db.commit()
            print('*'*50)
            print(mycursor.rowcount, 'record inserted')
            print('*'*50)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return redirect(url_for('home'))    

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# -----------------------------------------------------------------------------------

app.route('/clear_list', methods = ['GET', "POST"])
def clear_list():
    global answer_stats
    answer_stats = []

@app.route('/about-us')
def about_us():
    reset_quiz()
    return render_template('about-us.html')

@app.route('/community')
def community():
    reset_quiz()
    return render_template('community.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

# LOIGIN -> SIGNUP -> LOGOUT
@app.route('/login')
def login():
    return render_template('login.html')

# from news.py
session_user = []
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if request.method == 'POST':
        mycursor.execute(f"SELECT * FROM user_example WHERE email = '{email}'")
        current_user = mycursor.fetchall()

        print('*'*50)
        print(current_user, 'current_user var')
        print('*'*50)

        if not current_user[0][2] or not current_user[0][3]:
            flash("Please check your login details and try again.")
            return redirect(url_for('login'))
    
        session['user_id'] = current_user[0][0]
        session_user.append(current_user[0][0])
        session_info.append(session)
        print(session_info)
        print('*'*50)
        print('user session made')
        print('*'*50)
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    new_user_session = []
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        username = request.form.get('username')
        mycursor.execute(f"SELECT * FROM user_example WHERE email = '{email}' ")
        user_list = mycursor.fetchall()
        news.create_users(user_list, email=email, name=name, password=password, username=username)
        print('*'*50)
        print(user_list, "this is user_list")
        print('*'*50)
        mycursor.execute(f"SELECT * FROM user_example WHERE email = '{email}'")
        new_user_info = mycursor.fetchall()
        print('*'*50)
        print(new_user_info, 'this is new user info')
        print('*'*50)
        for i in new_user_info:
            new_user_session.append(i)
        print(new_user_session)
        session['user_id'] = user_list[0][0]
        return  redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/delete_session')
def delete_session():
    session.pop('user_id', default=None)
    print('*'*50)
    print(session_info, 'session info')
    print('*'*50)
    return redirect(url_for('home'))

# SECURED ROUTES
@app.route('/hello')
@auth.login_required
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
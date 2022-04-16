from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, request, session
from flask.helpers import flash
import numpy as np

myname = 'Juan'
import mysql.connector
weeb_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='weeb_db'
)
mycursor = weeb_db.cursor()

def create_users(users, email, name, password, username):
    if users:
        flash('Email address already exist')
        return redirect(url_for('signup'))

    sql_command = "INSERT INTO user_example(name, email, password, username) VALUES(%s, %s, %s, %s)"
    sql_values = (name, email, generate_password_hash(password, method='sha256'), username)
    
    mycursor.execute(sql_command, sql_values)
    weeb_db.commit()
    return redirect(url_for('login'))

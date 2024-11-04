# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# Indigo
# SoftDev
# P00: Move Slowly and Fix Things
# 2024-10-28
# Time spent: 5

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
import numpy as np
import sqlite3
import os 
from werkzeug.security import generate_password_hash, check_password_hash
import json

# import database

app = Flask(__name__)
CORS(app)
secret_key = os.urandom(32)
app.secret_key = os.environ.get('SECRET_KEY') or 'optional_default_key'

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username = session['username'])
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
       session['username'] = request.form['username']
       session['password'] = request.form['password'] 
        
        # # Function to check if username and password match:
        # if validate_login(username, password):
        #     session['username'] = username
        #     flash('Login successful!', 'success')
        #     user_data = fetch_user_data(username)
       return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        # Generate a password hash
        # password_hash = generate_password_hash(password)

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # database_path = os.path.join(basedir, 'db', 'users.db')
        # with sqlite3.connect(database_path) as conn:
        #     cur = conn.cursor()

        #     # Create the users table if it doesn't already exist
        #     cur.execute('''
        #         CREATE TABLE IF NOT EXISTS users (
        #             user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             username TEXT NOT NULL UNIQUE,
        #             password_hash TEXT NOT NULL
        #         );
        #     ''')

        #     # Insert the username and the hashed password into the database
        #     cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        #     conn.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/create', methods=['GET', 'POST'])
def create_story():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            title = request.form['title']
            edit = request.form['edit']

            basedir = os.path.abspath(os.path.dirname(__file__))
            database_path = os.path.join(basedir, 'db', 'users.db')
            with sqlite3.connect(database_path) as conn:
                cur = conn.cursor()
                
                user_id = cur.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()[0]

                cur.execute('''
                    CREATE TABLE IF NOT EXISTS stories (
                        story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        story_title TEXT NOT NULL UNIQUE
                    );
                ''')

                result = cur.execute("SELECT story_title from stories")
                all_stories = [row[0] for row in cur.fetchall()]
                
                if title in all_stories:
                    flash('Choose a different title, there is already a story with the same title!', 'error')
                else:
                    cur.execute("INSERT INTO stories (story_title) VALUES(?)", (title,))
                conn.commit()
                edit_story(user_id, title, edit)
                flash('Creation successful! You can now view your story on your homepage!', 'success')
            return redirect(url_for('home'))
        return render_template('create_story.html')
    else:
        flash('You must be logged in to create a story!', 'error')

if __name__ == "__main__":
    app.debug = True
    app.run()

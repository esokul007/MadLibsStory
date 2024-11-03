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

secret_key = os.urandom(24)
app.secret_key = os.environ.get('SECRET_KEY') or 'optional_default_key'

@app.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Generate a password hash
        password_hash = generate_password_hash(password)

        basedir = os.path.abspath(os.path.dirname(__file__))
        database_path = os.path.join(basedir, 'db', 'users.db')
        with sqlite3.connect(database_path) as conn:
            cur = conn.cursor()

            # Create the users table if it doesn't already exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                );
            ''')

            # Insert the username and the hashed password into the database
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()

def edit_story(user_id, title, edit):
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, 'db', 'users.db')
    with sqlite3.connect(database_path) as conn:
        cur = conn.cursor()

        result = cur.execute("SELECT story_id FROM stories WHERE story_title = ?", (title,))

        story_id = result.fetchone()[0]

        cur.execute('''
            CREATE TABLE IF NOT EXISTS story_edits (
                edit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT NOT NULL,
                story_id INT NOT NULL,
                edit TEXT NOT NULL
            );
        ''')

        cur.execute("INSERT INTO story_edits (user_id, story_id, edit) VALUES (?, ?, ?)", (user_id, story_id, edit))
        conn.commit()

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
                    cur.execute("INSERT INTO stories (story_title), VALUES(?)", (title,))
                conn.commit()
                edit_story(user_id, title, edit)
                flash('Creation successful! You can now view your story on your homepage!', 'success')
    else:
        flash('You must be logged in to create a story!', 'error')

@app.route('/edit', methods=['GET', 'POST'])
def create_edit():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            title = request.form['title']
            edit = request.form['edit']
            
            basedir = os.path.abspath(os.path.dirname(__file__))
            database_path = os.path.join(basedir, 'db', 'users.db')
            with sqlite3.connect(database_path) as conn:
                cur = conn.cursor()
                result = cur.execute("SELECT user_id from users WHERE username = ?", (username))
                user_id = result.fetchone()[0]
                
                result = cur.execute("SELECT story_id from story_edits WHERE user_id = ?", (user_id))
                user_edit_story_ids = [row[0] for row in cur.fetchall()]
                
                for story_id in user_edit_story_ids:
                    result = cur.execute("SELECT story_title from stories WHERE story_id = ?", (story_id))
                    story_title = result.fetchone()[0]
                    if story_title == title:
                        flash('You have already edited this story!', 'error')
                
                edit_story(user_id, title, edit)
                flash('Edit succesful! You can now view the full story!', 'success')
    else:
        flash('You must be logged in to edit a story!', 'error')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        
        # Function to check if username and password match:
        if validate_login(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            user_data = fetch_user_data(username)
            return redirect(url_for('home'))
    
    return render_template('SmartWordle.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

def validate_login(acc_username, password):
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, 'db', 'users.db')
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (acc_username,))
    user_password_hash = cur.fetchone()  # Fetches the first row of the query result
    conn.close()

    if user_password_hash:
        # Check if the password hash matches the hash of the entered password
        if check_password_hash(user_password_hash[0], password):
            return True
        else:
            flash('The password you entered is incorrect!', 'error')
            return False
    else:
        flash('Invalid username!', 'error')
        return False  

    
    
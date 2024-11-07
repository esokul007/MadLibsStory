# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# Indigo
# SoftDev
# P00: Move Slowly and Fix Things
# 2024-10-28
# Time spent: 12

from flask import request, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Database path setup
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')

# connext to database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # So I can access dictionary items using their column name instead of indexing
    return conn

# Creates new user in the database
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Create users table if it doesn't exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                );
            ''')
            # Insert new user into the database
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            flash('Registration successful!', 'success')
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
        finally:
            conn.close()

# Logs in user if username and password match
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        # Retrieve hashed password for the given username
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user_password_hash = cur.fetchone()
        conn.close()

        # Checks hashed user password against database
        if user_password_hash and check_password_hash(user_password_hash['password_hash'], password):
            session['username'] = username
            flash('Login successful!', 'success')
        else:
            flash('Invalid username or password!', 'error')

# Logs out user
def logout_user():
    session.pop('username', None)
    flash('You have been logged out.', 'success')

#  Create a new story if the user is logged in
def create_story():
    if 'username' in session:
        username = session['username']
        title = request.form['title']
        edit = request.form['edit']

        conn = get_db_connection()
        cur = conn.cursor()

        # Retrieve the user ID for the current session's username
        user_id = cur.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()[0]
        
        # Create stories table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_title TEXT NOT NULL UNIQUE,
                completed BOOLEAN DEFAULT False
            );
        ''')

        # Check if the story title already exists
        result = cur.execute("SELECT story_title FROM stories").fetchall()
        all_stories = [row['story_title'] for row in result]

        if title in all_stories:
            flash('Choose a different title, a story with this title already exists!', 'error')
            return False
        else:
            # Insert new story and commit changes
            cur.execute("INSERT INTO stories (story_title) VALUES(?)", (title,))
            conn.commit()
            create_edit(user_id, title, edit)
            flash('Story creation successful!', 'success')
        conn.close()
        return True
    else:
        flash('You must be logged in to create a story!', 'error')

# Create a new edit for a story
def create_edit(user_id, title, edit):
    conn = get_db_connection()
    cur = conn.cursor()

    # Retrieve story ID for the given title
    story_id = cur.execute("SELECT story_id FROM stories WHERE story_title = ?", (title,)).fetchone()[0]

    # Create story_edits table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS story_edits (
            edit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            edit TEXT NOT NULL
        );
    ''')
    # Insert the new edit
    cur.execute("INSERT INTO story_edits (user_id, story_id, edit) VALUES (?, ?, ?)", (user_id, story_id, edit))
    conn.commit()
    conn.close()

# Validate the user's login credentials
def validate_login(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    # Retrieve the hashed password from the database
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user_password_hash = cur.fetchone()
    conn.close()

    if user_password_hash and check_password_hash(user_password_hash['password_hash'], password):
        return True
    else:
        return False

# Returns different story for each type of info is wanted (ie. only completed stories for 3, only user edited stories for 2, etc.)
def get_stories(info_type):
    conn = get_db_connection()
    cur = conn.cursor()
    # Creates tables if they don't exist so I don't get errors when running with new database
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                );
            ''')
    cur.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_title TEXT NOT NULL UNIQUE,
                completed BOOLEAN DEFAULT False
            );
        ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS story_edits (
            edit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            edit TEXT NOT NULL
        );
    ''')
    # commit changes if they aren't tables
    conn.commit()
    
    # Retrieves all story info
    result = cur.execute("SELECT story_title, story_id, completed FROM stories").fetchall()
    
    # Gets the story titles and ids
    all_stories = [row['story_title'] for row in result]
    all_ids = [row['story_id'] for row in result]
    all_statuses = [row['completed'] for row in result]
    all_story_id_pairs = [(all_stories[i], all_ids[i], all_statuses[i]) for i in range(len(all_stories))]
    
    # Checks if user is logged in, will return different info
    if 'username' in session:
        username = session['username']
        user_id = cur.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()[0]
    else:
        user_id = -1
        
    # Get all edit history
    result = cur.execute("SELECT user_id, story_id, edit FROM story_edits").fetchall()
    all_user_ids = [row['user_id'] for row in result]
    all_story_ids = [row['story_id'] for row in result]
    all_edits = [row['edit'] for row in result]
    story_edits = {}
    user_edited_stories = []
    for i in range(len(all_edits)):
        if all_story_ids[i] not in story_edits:
            story_edits[all_story_ids[i]] = []
        story_edits[all_story_ids[i]].append(all_edits[i])
        if all_user_ids[i] == user_id:
            user_edited_stories.append(all_story_ids[i])
    conn.close()
    
    # All stories
    if info_type == 0:
        return all_story_id_pairs, story_edits, user_edited_stories
    # Stories in progress
    elif info_type == 1:
        new_pairs = []
        for story_pair in all_story_id_pairs:
            if story_pair[2] != True:
                new_pairs.append(story_pair)
        return new_pairs, story_edits, user_edited_stories
    # User edited stories
    elif info_type == 2:
        new_pairs = []
        for story_pair in all_story_id_pairs:
            if story_pair[1] in user_edited_stories:
                new_pairs.append(story_pair)
        return new_pairs, story_edits, user_edited_stories
    # Completed stories
    else:
        new_pairs = []
        for story_pair in all_story_id_pairs:
            if story_pair[2] == True:
                new_pairs.append(story_pair)
        return new_pairs, story_edits, user_edited_stories

# Determines whether or not user can add to the story
def can_add_to_story(story_id):
    if 'username' in session:
        username = session['username']
        conn = get_db_connection()
        cur = conn.cursor()
        user_id = cur.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()[0]
        result = cur.execute("SELECT user_id FROM story_edits WHERE story_id = ?", (story_id,)).fetchall()
        all_user_edit_ids = [row['user_id'] for row in result]
        completed = cur.execute("SELECT completed from stories WHERE story_id = ?", (story_id,)).fetchone()[0]
        conn.close()
        if user_id in all_user_edit_ids:
            return False, completed
        return True, completed

# Function to actually add to the story, along with updated status
def add_to_story(story_id, completed):
    edit = request.form['edit']
    if can_add_to_story(story_id):
        conn = get_db_connection()
        cur = conn.cursor()
        last_completed = cur.execute("SELECT completed from stories WHERE story_id = ?", (story_id,)).fetchone()[0]
        if last_completed == True:
            flash('You have already edited this story!', 'error')
            return False
        if 'username' in session:
            username = session['username']
            user_id = cur.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()[0]
        story_title = cur.execute("SELECT story_title FROM stories WHERE story_id = ?", (story_id,)).fetchone()[0]
        create_edit(user_id, story_title, edit)
        cur.execute("UPDATE stories SET completed = ? WHERE story_id = ?", (completed, story_id))
        conn.commit()
        conn.close()
        return True
    else:
        return False
        
# Returns the contributors for a specific story
def get_contributors(story_id):
    conn = get_db_connection()
    cur = conn.cursor()
    result = cur.execute("SELECT user_id FROM story_edits WHERE story_id = ?", (story_id,)).fetchall()
    all_users = [row['user_id'] for row in result]
    contributors = []
    for user in all_users:
        username = cur.execute("SELECT username FROM users WHERE user_id = ?", (user,)).fetchone()[0]
        contributors.append(username)
    conn.close()
    return contributors
    
    
    

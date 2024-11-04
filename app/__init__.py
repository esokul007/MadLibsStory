# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# Indigo
# SoftDev
# P00: Move Slowly and Fix Things
# 2024-10-28
# Time spent: 5

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json
from database import *

# import database

app = Flask(__name__)
secret_key = os.urandom(32)
app.secret_key = os.environ.get('SECRET_KEY') or 'optional_default_key'

# Home route
@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        # Fetch user data from the database using username
        letter_freq, user_data, num_games = fetch_user_data(username)
        # Render a template with user-specific data
        return render_template('home.html', username=username)
    else:
        # If no user is logged in, just render the template without user-specific data
        return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    create_user()
    return render_template('register.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

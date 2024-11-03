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

import database

app = Flask(__name__)
CORS(app)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

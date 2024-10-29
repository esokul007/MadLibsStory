# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# Indigo
# SoftDev
# P00: Move Slowly and Fix Things
# 2024-10-28
# Time spent: XXXXXXX

from flask import Flask, request, render_template, make_response, redirect, url_for
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

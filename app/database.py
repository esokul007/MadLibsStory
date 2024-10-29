from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json
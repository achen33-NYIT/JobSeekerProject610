from app import app
import pymysql
from app import app
from app.dbconfig import mysql
from flask import jsonify
#from flask_jwt import jwt, jwt_required, current_identity
# from werkzeug.security import generate_password_hash, check_password_hash

def login(): 
    return 0

def register(email, username, password):
    
    return jsonify(email=email,username=username,password=password)
from app import app
import pymysql
from app import app
from app.dbconfig import mysql
from flask import jsonify,make_response
from flask_jwt import jwt, jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash

def login(email, password): 
    conn = None
    cursor = None
    try:
         
        _email = email
        _password = password
        _hashed_password = generate_password_hash(_password)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print(_hashed_password)
        query = "select * from user where email = %s"
        data =(_email)
        cursor.execute(query,data)
        row =  cursor.fetchone()
        print (row)
        if(row == None):
           print ("no user found!!");
        else:   
           print ("done")
    except Exception as e:
        print(e);
        return "something went wrong"
    return "ended"
    
def register(fname,lname,email, password):
    conn = None
    cursor = None
    _email = email
    _password = password
    _fname = fname
    _lname = lname
    try: 
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
    
        query = "select * from user where email = %s"
        data =(_email)
        cursor.execute(query,data)
        row =  cursor.fetchone()
        print (row)
        if(row == None):
           print ("no user found!!")
        else:   
           return "user exist"
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()        

    try:        
        _hashed_password = generate_password_hash(_password)
        query = "insert into user(FirstName,LastName,email,password) values(%s,%s,%s,%s)"
        data =(_fname,_lname,_email,_hashed_password)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query,data)
        conn.commit()
        response = make_response(
                jsonify(
                    {"message": "success"}
                ),
                200,
            )
        response.headers["Content-Type"] = "application/json"

        return response 
    except Exception as e:
        print(e)
        return "Something went wrong"
    finally:
        cursor.close() 
        conn.close()
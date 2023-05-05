# app root

from app import app
from repos.api import ChatGPT

from flask import Flask, render_template, request
from flask import Flask, jsonify, render_template, request
from wtforms import Form, TextAreaField, validators
from app.controller import loginController,ResumeController
from flask_cors import CORS

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
class ReviewForm(Form):
    jobreview = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])

# TODO: store in central datastore or call from API directly
results = [
    {"role": "system", "content": "You recommend jobs to job candidates based on their skills"}
]


# @app.route('/', methods=['POST', 'GET'])
@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        return loginController.login(email,password)
    else:
        return "failed"
      
@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        
        return loginController.register(fname,lname,email,password)
    else:
        return "failed"

@app.route('/chatgpt', methods=['POST'])
def index():
    results = None
    if request.method == 'GET':
        # Use the list of all languages
        results = [
            {"role": "system", "content": "You recommend jobs to job candidates based on their skills"}
            ]
    elif request.method == 'POST':
        # Use the languages we selected in the request form
        user_input = request.form["variable"]

        results = ChatGPT(user_input)
    return render_template('index.html', results=results)

@app.route('/upload', methods=['POST'])
def upload_resume():
    upload_resume = request.files['file']
    print(upload_resume)
    if upload_resume.filename != '':
        upload_resume.save(upload_resume.filename)
        res = ResumeController.submit_data(upload_resume.filename)
        return res
    else:
        print("no file")
        res.emptyFile = True
        return res
    
@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['jobreview']
        return render_template('results.html')
    return render_template('reviewform.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
    return render_template('thanks.html')

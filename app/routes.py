# app root

from app import app
from repos.api import ChatGPT
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

@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        return loginController.login(email,password);
    else:
        return "failed"
      
@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        
        return loginController.register(fname,lname,email,password);
    else:
        return "failed"

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

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


@app.route('/chatgpt',methods=["POST"])
def chatgpt():
    if request.method == 'POST':
        # Use the languages we selected in the request form
        user_input = request.get_json()['jobtitle'];
        print(user_input)
        str = "suggest me skills required for " + user_input
        results = ChatGPT(str)

        print(jsonify(results))
        return jsonify(results)
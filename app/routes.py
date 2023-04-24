# app root

from app import app
from repos.api import ChatGPT

from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

class ReviewForm(Form):
    jobreview = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])

# TODO: store in central datastore or call from API directly
results = [
    {"role": "system", "content": "You recommend jobs to job candidates based on their skills"}
]


@app.route('/', methods=['POST', 'GET'])
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
# app root

from app import app

from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

class ReviewForm(Form):
    jobreview = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

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
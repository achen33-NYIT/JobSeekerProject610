from flask import Flask

app = Flask(__name__)

from app import routes

app.config['SECRET_KEY'] = 'Y6X9zGuWeI'


app.run(debug=True, port = 4000)
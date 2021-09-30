from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
## App Instance
app = Flask(__name__)



## Home Page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add-note')
def add():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
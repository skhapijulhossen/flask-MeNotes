from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime
from flask import session
import os
from datetime import datetime
# App Instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/happy/OneDrive/Dev/flask-MeNotes/notes.db'

db = SQLAlchemy(app)
app.secret_key = os.urandom(16)


# Creating Table
class Users(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Note(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(55), unique=True, nullable=False)
    body = Column(Text(convert_unicode=True), nullable=False)
    author = Column(String(25), nullable=False)
    date = Column(DateTime())


# Home Page
@app.route('/')
def index():
    if 'username' in session:
        if 'view' in session:
            user = session['username']
            notes = Note.query.filter_by(author=user).all()
            viewNote = Note.query.filter_by(id=session['view']).first()
            return render_template('index.html', user=user, notes=notes[::-1], viewNote=viewNote)
        user = session['username']
        notes = Note.query.filter_by(author=user).all()
        print(notes[::-1])
        return render_template('index.html', user=user, notes=notes[::-1], viewNote=None)
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].replace(' ', '')
        email = request.form['email'].replace(' ', '')
        password = request.form['password'].replace(' ', '')
        user = Users(
            username=username,
            email=email,
            password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        print(user.password)
        if user and (user.password == password):
            session['username'] = user.username
            print(session.items())
            return redirect(url_for('index', usr=user))
        else:
            return redirect('/signup')

    return render_template('login.html')


@app.route('/add-note', methods=['GET', 'POST'])
def add():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            author = session['username']
            date = datetime.now()
            note = Note(title=title, body=body, author=author, date=date)
            print(note.title)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('addnote.html')
    return redirect(url_for('signup'))


@app.route('/view/<int:id>')
def view(id):
    # remove the username from the session if it's there
    session['view'] = id
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    # remove the username from the session if it's there
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    session.pop('view', None)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('view', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

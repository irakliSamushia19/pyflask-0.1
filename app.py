from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'lecture14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fortest.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __str__(self):
        return f'first_name:{self.first_name}; last_name: {self.last_name}; gender: {self.gender}; email: {self.email}; password: {self.password}'


@app.route('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' not in session:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            gender = request.form.getlist('gender')
            email = request.form['email']
            password = request.form['password']
            b1 = Person(first_name=first_name, last_name=last_name, gender='male', email=email, password=password)
            db.session.add(b1)
            db.session.commit()
            log_password = request.form['log_password']
            log_name = request.form['log_name']
            if log_name == '' or log_password == '':
                flash('შეიყვანეთ ინფორმაცია')
                return render_template('login.html')
            else:
                login = Person.query.filter_by(email=log_name, password=log_password).first()
                if login is None:
                    flash('მომხმარებელი არ არის დარეგისტრირებული')
                    return render_template('login.html')
                else:
                    session['email'] = log_name
                    return redirect(url_for('home'))
        return render_template('login.html')
    else:
        return redirect(url_for('home'))


# emails = Person.query.all()
# for each in emails:
#     print(each)


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/user')
def user():
    return render_template('user.html')


# @app.route('/admin')
# def admin():
#     return redirect('/')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)


# conn = sqlite3.connect('fortest.sqlite')
# cursor = conn.cursor()
# dell = ("DELETE FROM Person where gender='male'")
# cursor.execute(dell)
# conn.commit()

















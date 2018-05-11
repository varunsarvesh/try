from flask import Flask, render_template, url_for, redirect, session, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'something'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/sign'
db = SQLAlchemy(app)

class Users(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(250))



@app.route('/')
def index():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signed_up', methods=['POST', 'GET'])
def signed():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['pass']
        email = request.form['email']
        check = Users.query.filter_by(username=name).first()
        if check:
            flash('The username already available')
            return redirect(url_for('signup'))
        users = Users(username=name, password=password, email=email)
        db.session.add(users)
        db.session.commit()
        flash("successfully signed up",)
    return redirect(url_for('index'))


@app.route('/logged', methods=['POST', 'GET'])
def logged():
    if request.method == 'POST':
        name = request.form['id']
        password = request.form['pass']
        session['id'] = name
        check = Users.query.filter_by(username=name).first()
        if check:
            if check.username != password:
                flash('incorrect password')
                return redirect(url_for('index'))
        else:
            flash('no user id found')
            return redirect(url_for('index'))
    if 'id' not in session:
        flash("log in to access")
        return redirect(url_for('index'))
    return session['id']+', Dude there is nothing to log in <br><a href=\'/logout\'><h1>Click to log out</a>'
    # return f"{idd} Dude there is nothing to log in <br><a href='/logout'><h1>Click to log out</a>"


@app.route('/logout')
def logout():
    session.pop('id', None)
    return "You have logged out <br><a href='/'><h1> Home page</a>"


if __name__ == '__main__':
    app.run(debug=True)

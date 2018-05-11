from flask import Flask, render_template, url_for, redirect, session, request, flash
from models import db, Users


app = Flask(__name__)
app.secret_key = 'something'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/sign'
db.init_app(app)


def valid(name: str, password: str, email: str) -> bool:
    if len(password) == 0 or len(email) == 0 or len(name) == 0:
        return False
    else:
        return True


def create_entry(name: str, password: str, email: str):
    users = Users(username=name, password=password, email=email)
    db.session.add(users)
    db.session.commit()


def check_username(name: str):
    check = Users.query.filter_by(username=name).first()
    if check:
        return True
    else:
        return False


def match(name: str, password: str):
    check = Users.query.filter_by(username=name).first()
    if check.password == password:
        return True
    else:
        return False


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
        if not valid(name, password, email):
            flash('Entries cannot be left blank')
            return redirect(url_for('signup'))
        if check_username(name):
            flash('The username already available')
            return redirect(url_for('signup'))
        create_entry(name, password, email)
        flash("successfully signed up", )
    return redirect(url_for('index'))


@app.route('/logged', methods=['POST', 'GET'])
def logged():
    if request.method == 'POST':
        name = request.form['id']
        password = request.form['pass']
        session['id'] = name
        if check_username(name):
            if not match(name, password):
                flash('incorrect password')
                return redirect(url_for('index'))
        else:
            flash('no user id found')
            return redirect(url_for('index'))
    if 'id' not in session:
        flash("log in to access")
        return redirect(url_for('index'))
    # return session['id']+', Dude there is nothing to log in <br><a href=\'/logout\'><h1>Click to log out</a>'
    return f"{idd} Dude there is nothing to log in <br><a href='/logout'><h1>Click to log out</a>"


@app.route('/logout')
def logout():
    session.pop('id', None)
    return "You have logged out <br><a href='/'><h1> Home page</a>"


if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, render_template, request, redirect, url_for, flash, session
#pip install pyopenssl
from handler.databasehandler import create_structure, login_request, register_request, add_request, passwords_request, remove_request


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
create_structure()


@app.route('/')
def index():
    if 'username' in session:
        data = passwords_request(session['username'])
        return render_template('index.html', username=session['username'], data=data)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if login_request(username, password):
        session['username'] = username
        session['password'] = password
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    if login_request(username, password):
        flash('User already exists')
        return redirect(url_for('register'))
    else:
        if register_request(username, password):
            flash('User created')
            return redirect(url_for('login'))
        else:
            flash('Error creating user')
            return redirect(url_for('register'))
        
@app.route('/add')
def add():
    if 'username' in session:
        return render_template('add.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/add', methods=['POST'])
def add_entry():
    if 'username' in session:
        username = session['username']
        password = session['password']
        if login_request(username, password):
            if add_request(username, request.form['service'], request.form['email'], request.form['password'], request.form['url']):
                flash('Password added')
                return redirect(url_for('index'))
            else:
                flash('Error adding password')
        else:
            flash('Session expired')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
        
@app.route('/remove', methods=['POST'])
def remove_entry():
    if 'username' in session:
        username = session['username']
        password = session['password']
        if login_request(username, password):
            if remove_request(username, request.form['id']):
                flash('Password deleted!')
                return redirect(url_for('index'))
            else:
                flash('Error deleting password')
        else:
            flash('Session expired')
            return redirect(url_for('login'))
    else:
        flash('Session expired')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run( debug=True)
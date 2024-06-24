from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {'user': 'pass'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('game'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'User already exists'
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(1, 100)
        session['attempts'] = 0
    
    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] += 1
        if guess < session['secret_number']:
            feedback = 'Higher'
        elif guess > session['secret_number']:
            feedback = 'Lower'
        else:
            feedback = f'Correct! You guessed it in {session["attempts"]} attempts'
            session.pop('secret_number')
            session.pop('attempts')
    else:
        feedback = ''
    
    return render_template('game.html', feedback=feedback)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

# test_app.py - STANDALONE TEST
from flask import Flask, render_template, request, redirect, session, flash
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'test-secret-key-123'

# Simple in-memory user storage (replace with your database)
users = {}

# Routes
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill all fields', 'error')
            return render_template('login.html')
        
        # Simple check (replace with database)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # For demo - auto create user if not exists
        if email not in users:
            users[email] = {
                'name': 'Test User',
                'password': hashed_password,
                'email': email
            }
        
        if users[email]['password'] == hashed_password:
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([fullname, email, password, confirm_password]):
            flash('Please fill all fields', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        
        if email in users:
            flash('Email already registered!', 'error')
            return render_template('signup.html')
        
        # Create user
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users[email] = {
            'name': fullname,
            'password': hashed_password,
            'email': email
        }
        
        session['user_email'] = email
        session['user_name'] = fullname
        flash('Account created successfully!', 'success')
        return redirect('/dashboard')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect('/login')
    
    return f'''
    <html>
    <head>
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="#">TMS Dashboard</a>
                <div class="navbar-nav ms-auto">
                    <span class="navbar-text me-3">Welcome, {session['user_name']}</span>
                    <a class="btn btn-outline-light btn-sm" href="/logout">Logout</a>
                </div>
            </div>
        </nav>
        <div class="container mt-4">
            <h1>Welcome to TMS!</h1>
            <p>You are successfully logged in as: {session['user_email']}</p>
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Transport Management System</h5>
                    <p class="card-text">Your authentication is working perfectly!</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# app.py - CLEAN WORKING VERSION
from flask import Flask, render_template, request, redirect, session, flash
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tms-secret-key-2024'

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)

# Simple user storage (replace with database later)
users = {}

# ========================
# ROUTES
# ========================

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
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # For demo - auto create user if not exists
        if email not in users:
            users[email] = {
                'name': 'Demo User',
                'password': hashed_password,
                'email': email
            }
        
        if users[email]['password'] == hashed_password:
            session['user_id'] = email
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email or password!', 'error')
    
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
        
        session['user_id'] = email
        session['user_email'] = email
        session['user_name'] = fullname
        
        flash('Account created successfully!', 'success')
        return redirect('/dashboard')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    return render_template('dashboard.html',
                         user_name=session.get('user_name'),
                         user_email=session.get('user_email'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect('/login')

# ========================
# MAIN
# ========================

if __name__ == '__main__':
    print('🚀 TMS Application Starting...')
    print('📍 Login: http://127.0.0.1:5000/login')
    print('📍 Signup: http://127.0.0.1:5000/signup')
    print('📍 Dashboard: http://127.0.0.1:5000/dashboard')
    print('')
    print('⚡ If you see connection refused, try these URLs:')
    print('📍 http://localhost:5000')
    print('📍 http://192.168.75.67:5000')
    print('')
    app.run(debug=True, host='0.0.0.0', port=5000)

# app/auth_routes.py - GUARANTEED WORKING AUTH
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import hashlib
from database.db import get_db_connection

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# LOGIN ROUTES
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Please fill all fields', 'error')
                return render_template('login.html')
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Check user
            cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, hashed_password))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_name'] = user.get('name', 'User')
                flash('Login successful!', 'success')
                return redirect('/dashboard')  # Change to your main page
            else:
                flash('Invalid email or password!', 'error')
                
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
    
    return render_template('login.html')

# SIGNUP ROUTES
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
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
            
            if len(password) < 6:
                flash('Password must be at least 6 characters', 'error')
                return render_template('signup.html')
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('Email already registered!', 'error')
                cursor.close()
                conn.close()
                return render_template('signup.html')
            
            # Create new user
            cursor.execute(
                'INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, NOW())',
                (fullname, email, hashed_password)
            )
            conn.commit()
            
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            # Auto login after signup
            session['user_id'] = user_id
            session['user_email'] = email
            session['user_name'] = fullname
            
            flash('Account created successfully!', 'success')
            return redirect('/dashboard')  # Change to your main page
            
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'error')
    
    return render_template('signup.html')

# LOGOUT ROUTE
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect('/login')

# Simple dashboard for testing
@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    return f'''
    <html>
    <head><title>Dashboard</title></head>
    <body>
        <h1>Welcome {session.get('user_name')}!</h1>
        <p>Email: {session.get('user_email')}</p>
        <p><a href="/logout">Logout</a></p>
    </body>
    </html>
    '''

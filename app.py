# app.py - TMS WITH SQLITE DATABASE
from flask import Flask, render_template, request, redirect, session, flash
import hashlib
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tms-secret-key-2024'

# SQLite database configuration
DATABASE = 'tms_database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    '''Initialize the database with required tables'''
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create vehicles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT UNIQUE NOT NULL,
            model TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample vehicles
    cursor.execute('''
        INSERT OR IGNORE INTO vehicles (plate_number, model, capacity, status) 
        VALUES 
        ('DHK-12345', 'Toyota Hiace', 12, 'Active'),
        ('CTG-67890', 'Mitsubishi L300', 10, 'Active'),
        ('KHL-11223', 'Nissan Civilian', 15, 'Maintenance')
    ''')
    
    conn.commit()
    conn.close()
    print('✅ Database initialized with sample data')

# Initialize database
init_db()

# Ensure templates directory exists
os.makedirs('templates', exist_ok=True)

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
        
        try:
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE email = ? AND password = ?', 
                (email, hashed_password)
            ).fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_name'] = user['name']
                flash('Login successful!', 'success')
                return redirect('/dashboard')
            else:
                flash('Invalid email or password!', 'error')
                
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
    
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
        
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            conn = get_db_connection()
            
            # Check if user exists
            existing_user = conn.execute(
                'SELECT id FROM users WHERE email = ?', (email,)
            ).fetchone()
            
            if existing_user:
                flash('Email already registered!', 'error')
                conn.close()
                return render_template('signup.html')
            
            # Create new user
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                (fullname, email, hashed_password)
            )
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Auto login
            session['user_id'] = user_id
            session['user_email'] = email
            session['user_name'] = fullname
            flash('Account created successfully!', 'success')
            return redirect('/dashboard')
            
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'error')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    # Get stats from database
    try:
        conn = get_db_connection()
        vehicles_count = conn.execute('SELECT COUNT(*) FROM vehicles').fetchone()[0]
        active_vehicles = conn.execute('SELECT COUNT(*) FROM vehicles WHERE status = \"Active\"').fetchone()[0]
        conn.close()
    except:
        vehicles_count = 3
        active_vehicles = 2
    
    return render_template('dashboard.html',
                         user_name=session.get('user_name'),
                         user_email=session.get('user_email'),
                         vehicles_count=vehicles_count,
                         active_vehicles=active_vehicles)

@app.route('/vehicles')
def vehicles():
    if 'user_id' not in session:
        return redirect('/login')
    
    try:
        conn = get_db_connection()
        vehicles = conn.execute('SELECT * FROM vehicles ORDER BY created_at DESC').fetchall()
        conn.close()
    except Exception as e:
        vehicles = []
        flash(f'Error loading vehicles: {str(e)}', 'error')
    
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        plate_number = request.form.get('plate_number')
        model = request.form.get('model')
        capacity = request.form.get('capacity')
        
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO vehicles (plate_number, model, capacity) VALUES (?, ?, ?)',
                (plate_number, model, capacity)
            )
            conn.commit()
            conn.close()
            flash('Vehicle added successfully!', 'success')
            return redirect('/vehicles')
        except Exception as e:
            flash(f'Error adding vehicle: {str(e)}', 'error')
    
    return render_template('add_vehicle.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect('/login')

if __name__ == '__main__':
    print('🚀 TMS Application Starting...')
    print('📍 Login: http://127.0.0.1:5000/login')
    print('📍 Signup: http://127.0.0.1:5000/signup') 
    print('📍 Dashboard: http://127.0.0.1:5000/dashboard')
    print('📍 Vehicles: http://127.0.0.1:5000/vehicles')
    print('')
    print('💾 Using SQLite database: tms_database.db')
    app.run(debug=True, host='0.0.0.0', port=5000)

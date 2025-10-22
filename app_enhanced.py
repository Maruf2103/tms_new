# app_enhanced.py - Enhanced UAP-TMS with all features
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
import os
from datetime import datetime

# Import our new enhancement modules
from realtime_tracking import tracker
from payment_system import payment_processor
from registration_enhancements import registration_enhancer
from api_extensions import api_ext

app = Flask(__name__)
app.secret_key = 'uap-tms-enhanced-secret-key-2024'

# Register API extensions blueprint
app.register_blueprint(api_ext, url_prefix='/ext')

# Database setup
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('uap_tms.db')
    c = conn.cursor()
    
    # Existing tables (compatible with your current structure)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            department TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            route TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            capacity INTEGER,
            available_seats INTEGER
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bus_id INTEGER,
            registration_date TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')
    
    # Insert demo data
    # Demo users
    demo_users = [
        ('student1', 'password123', 'student', 'Samia Zaman', 'samia@uap.com', '017XXXXXXXX', 'CSE'),
        ('faculty1', 'password123', 'faculty', 'Dr. Atia Rahman', 'atia@uap.com', '018XXXXXXXX', 'CSE'),
        ('admin1', 'admin123', 'admin', 'Transport Admin', 'admin@uap.com', '019XXXXXXXX', 'Transport')
    ]
    
    c.executemany('''
        INSERT OR IGNORE INTO users (username, password, user_type, full_name, email, phone, department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', demo_users)
    
    # Demo buses
    demo_buses = [
        ('UAP-BUS-01', 'Mirpur to UAP Campus', '08:00 AM', 40, 35),
        ('UAP-BUS-02', 'Dhanmondi to UAP Campus', '08:30 AM', 40, 28),
        ('UAP-BUS-03', 'Gulshan to UAP Campus', '09:00 AM', 40, 40),
        ('UAP-BUS-04', 'UAP to Mirpur', '04:00 PM', 40, 32),
        ('UAP-BUS-05', 'UAP to Dhanmondi', '04:30 PM', 40, 40)
    ]
    
    c.executemany('''
        INSERT OR IGNORE INTO buses (bus_number, route, departure_time, capacity, available_seats)
        VALUES (?, ?, ?, ?, ?)
    ''', demo_buses)
    
    conn.commit()
    conn.close()
    print("? Database initialized with demo data")

# Initialize database and demo data when app starts
init_db()

# Existing routes (compatible with your current routes)
@app.route('/')
def home():
    """Home page"""
    return render_template('home_enhanced.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('uap_tms.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['user_type'] = user[3]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form.get('department', '')
        
        try:
            conn = sqlite3.connect('uap_tms.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (username, password, user_type, full_name, email, phone, department)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, password, user_type, full_name, email, phone, department))
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user info
    conn = sqlite3.connect('uap_tms.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    
    # Get available buses
    c.execute('SELECT * FROM buses WHERE available_seats > 0')
    buses = c.fetchall()
    
    # Get user registrations
    c.execute('''
        SELECT r.*, b.bus_number, b.route, b.departure_time 
        FROM registrations r 
        JOIN buses b ON r.bus_id = b.id 
        WHERE r.user_id = ?
    ''', (session['user_id'],))
    registrations = c.fetchall()
    
    conn.close()
    
    return render_template('dashboard_enhanced.html', 
                         user=user, 
                         buses=buses, 
                         registrations=registrations,
                         bus_locations=tracker.get_all_locations())

@app.route('/bus/register/<int:bus_id>')
def register_bus(bus_id):
    """Register for a bus"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conn = sqlite3.connect('uap_tms.db')
        c = conn.cursor()
        
        # Check if already registered
        c.execute('SELECT * FROM registrations WHERE user_id = ? AND bus_id = ?', 
                 (session['user_id'], bus_id))
        existing = c.fetchone()
        
        if existing:
            flash('You are already registered for this bus!', 'error')
        else:
            # Register user
            c.execute('''
                INSERT INTO registrations (user_id, bus_id, registration_date, status)
                VALUES (?, ?, ?, ?)
            ''', (session['user_id'], bus_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'confirmed'))
            
            # Update available seats
            c.execute('UPDATE buses SET available_seats = available_seats - 1 WHERE id = ?', (bus_id,))
            
            conn.commit()
            flash('Bus registration successful!', 'success')
        
        conn.close()
    except Exception as e:
        flash(f'Registration error: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# New enhanced routes
@app.route('/live-tracking')
def live_tracking():
    """Live bus tracking page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('live_tracking.html')

@app.route('/payment')
def payment_page():
    """Payment page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('payment.html')

@app.route('/routes-suggestions')
def route_suggestions():
    """Route suggestions page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('uap_tms.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    department = user[7] if user and len(user) > 7 else 'CSE'  # department is at index 7
    suggestions = registration_enhancer.suggest_routes(department, 'morning')
    
    return render_template('route_suggestions.html', 
                         suggestions=suggestions, 
                         department=department)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))

# API route for system status
@app.route('/api/status')
def api_status():
    """API endpoint to check system status"""
    return jsonify({
        'status': 'operational',
        'service': 'UAP-TMS Enhanced',
        'version': '2.0',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'real_time_tracking': True,
            'online_payments': True,
            'smart_routing': True,
            'live_updates': True
        }
    })

# Simple route to test the app
@app.route('/test')
def test():
    return jsonify({"message": "UAP-TMS is working!", "status": "success"})

if __name__ == '__main__':
    print("?? Starting UAP-TMS Enhanced Server...")
    print("?? Access your application at: http://127.0.0.1:5000")
    print("?? API Status: http://127.0.0.1:5000/api/status")
    print("?? Live Tracking: http://127.0.0.1:5000/live-tracking")
    print("?? Payment System: http://127.0.0.1:5000/payment")
    print("??? Route Suggestions: http://127.0.0.1:5000/routes-suggestions")
    print("?? Test Route: http://127.0.0.1:5000/test")
    
    # Run on port 5000 (Flask default) to avoid conflicts
    app.run(debug=True, host='127.0.0.1', port=5000)

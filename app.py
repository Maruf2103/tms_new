from flask import Flask, redirect
from app.auth.routes import auth_bp  # ADD THIS IMPORT

app = Flask(__name__)
app.secret_key = 'tms-production-secret-2024'  # ADD SECRET KEY

# Register blueprints
app.register_blueprint(auth_bp)  # ADD THIS REGISTRATION

# Root route - redirect to login
@app.route('/')
def index():
    return redirect('/login')

# Your existing routes below...
# app.py - UAP TMS with Complete Authentication
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'uap-tms-secure-key-2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect('uap_tms.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            department TEXT,
            student_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Buses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            route TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            capacity INTEGER DEFAULT 40,
            available_seats INTEGER,
            driver_name TEXT,
            driver_phone TEXT
        )
    ''')
    
    # Registrations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bus_id INTEGER,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'confirmed',
            payment_status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')
    
    # Insert demo users - FIXED: Use None instead of NULL
    demo_users = [
        ('student1', hash_password('password123'), 'student', 'Samia Zaman', 'samia@uap.edu.bd', '01700123456', 'CSE', '23101174'),
        ('student2', hash_password('password123'), 'student', 'Zakir Hossain', 'zakir@uap.edu.bd', '01700123457', 'CSE', '23101177'),
        ('student3', hash_password('password123'), 'student', 'Retu Islam', 'retu@uap.edu.bd', '01700123458', 'EEE', '23101187'),
        ('faculty1', hash_password('password123'), 'faculty', 'Dr. Atia Rahman', 'atia.rahman@uap.edu.bd', '01800123456', 'CSE', None),
        ('admin1', hash_password('admin123'), 'admin', 'Transport Admin', 'transport@uap.edu.bd', '01900123456', 'Transport', None)
    ]
    
    for user in demo_users:
        c.execute('''
            INSERT OR IGNORE INTO users (username, password, user_type, full_name, email, phone, department, student_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', user)
    
    # Insert demo buses
    demo_buses = [
        ('UAP-BUS-01', 'Mirpur to UAP Campus', '08:00 AM', 40, 25, 'Abdul Karim', '01700123459'),
        ('UAP-BUS-02', 'Dhanmondi to UAP Campus', '08:30 AM', 40, 18, 'Mohammad Ali', '01700123460'),
        ('UAP-BUS-03', 'Gulshan to UAP Campus', '09:00 AM', 40, 40, 'Rahim Khan', '01700123461'),
        ('UAP-BUS-04', 'UAP to Mirpur', '04:00 PM', 40, 32, 'Abdul Karim', '01700123459'),
        ('UAP-BUS-05', 'UAP to Dhanmondi', '04:30 PM', 40, 40, 'Mohammad Ali', '01700123460')
    ]
    
    for bus in demo_buses:
        c.execute('''
            INSERT OR IGNORE INTO buses (bus_number, route, departure_time, capacity, available_seats, driver_name, driver_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', bus)
    
    conn.commit()
    conn.close()
    print("? Database initialized with demo data")

# Initialize database
init_db()

# Authentication routes
@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration/sign up"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form.get('department', '')
        student_id = request.form.get('student_id', '')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('signup.html')
        
        try:
            conn = sqlite3.connect('uap_tms.db')
            c = conn.cursor()
            
            # Check if username already exists
            c.execute('SELECT id FROM users WHERE username = ?', (username,))
            if c.fetchone():
                flash('Username already exists! Please choose another.', 'error')
                return render_template('signup.html')
            
            # Insert new user
            hashed_password = hash_password(password)
            c.execute('''
                INSERT INTO users (username, password, user_type, full_name, email, phone, department, student_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, user_type, full_name, email, phone, department, student_id))
            
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login to continue.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('uap_tms.db')
        c = conn.cursor()
        
        # Get user with hashed password check
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and user[2] == hash_password(password):  # user[2] is password field
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['user_type'] = user[3]
            session['full_name'] = user[4]
            flash(f'Welcome back, {user[4]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('uap_tms.db')
    c = conn.cursor()
    
    # Get available buses
    c.execute('SELECT * FROM buses WHERE available_seats > 0')
    buses = c.fetchall()
    
    # Get user's registrations
    c.execute('''
        SELECT r.*, b.bus_number, b.route, b.departure_time 
        FROM registrations r 
        JOIN buses b ON r.bus_id = b.id 
        WHERE r.user_id = ?
        ORDER BY r.registration_date DESC
    ''', (session['user_id'],))
    registrations = c.fetchall()
    
    # Get user info
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         user=user, 
                         buses=buses, 
                         registrations=registrations,
                         full_name=session.get('full_name'))

@app.route('/bus/register/<int:bus_id>')
def register_bus(bus_id):
    """Register for a bus"""
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = sqlite3.connect('uap_tms.db')
        c = conn.cursor()
        
        # Check if already registered
        c.execute('SELECT * FROM registrations WHERE user_id = ? AND bus_id = ?', 
                 (session['user_id'], bus_id))
        existing = c.fetchone()
        
        if existing:
            flash('You are already registered for this bus!', 'warning')
        else:
            # Register user for bus
            c.execute('''
                INSERT INTO registrations (user_id, bus_id, status)
                VALUES (?, ?, ?)
            ''', (session['user_id'], bus_id, 'confirmed'))
            
            # Update available seats
            c.execute('UPDATE buses SET available_seats = available_seats - 1 WHERE id = ?', (bus_id,))
            
            conn.commit()
            
            # Get bus info for success message
            c.execute('SELECT bus_number, route FROM buses WHERE id = ?', (bus_id,))
            bus = c.fetchone()
            flash(f'Successfully registered for {bus[0]} - {bus[1]}!', 'success')
        
        conn.close()
    except Exception as e:
        flash(f'Registration error: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('uap_tms.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))

# API routes
@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "operational",
        "service": "UAP-TMS",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "authentication": "enabled"
    })

if __name__ == '__main__':
    print("?? UAP-TMS with Authentication Starting...")
    print("?? Home: http://127.0.0.1:5000")
    print("?? Login: http://127.0.0.1:5000/login")
    print("?? Sign Up: http://127.0.0.1:5000/signup")
    print("?? Dashboard: http://127.0.0.1:5000/dashboard")
    print("? Ready to use!")
    app.run(debug=True, host='127.0.0.1', port=5000)


# Add this if not present in original
if __name__ == '__main__':
    app.run(debug=True)

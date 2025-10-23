# check_auth.py - Diagnostic script
from flask import Flask
import os

app = Flask(__name__)

# Try to import and check routes
try:
    # Check if auth routes exist
    from app.routes import auth_routes
    print("✅ Auth routes module found")
    
    # Register blueprint if not already done
    app.register_blueprint(auth_routes)
    print("✅ Auth blueprint registered")
    
except ImportError as e:
    print(f"❌ Auth routes not found: {e}")
    
    # Create basic auth routes
    print("🛠 Creating basic auth routes...")
    from flask import Blueprint, render_template, redirect, url_for, request, flash
    
    auth_bp = Blueprint('auth', __name__)
    
    @auth_bp.route('/login')
    def login():
        return render_template('login.html')
    
    @auth_bp.route('/signup')
    def signup():
        return render_template('signup.html')
    
    @auth_bp.route('/logout')
    def logout():
        return redirect(url_for('auth.login'))
    
    app.register_blueprint(auth_bp)
    print("✅ Basic auth routes created and registered")

# Check templates
templates_dir = 'templates'
auth_templates = ['login.html', 'signup.html']
for template in auth_templates:
    template_path = os.path.join(templates_dir, template)
    if os.path.exists(template_path):
        print(f"✅ Template found: {template}")
    else:
        print(f"❌ Template missing: {template}")

print("Diagnostic complete!")

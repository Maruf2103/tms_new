import os
import glob

# Find all Python files that might be the main app
possible_files = glob.glob('*.py') + glob.glob('app/*.py') + glob.glob('*/__init__.py')

print("Looking for main Flask app file...")
for file in possible_files:
    print(f"Checking: {file}")
    
print("\n📝 INSTRUCTIONS:")
print("1. Find your main Flask app file (usually app.py, main.py, or app/__init__.py)")
print("2. Add these lines at the top with other imports:")
print("   from app.auth_routes import auth_bp")
print("3. Add this line after creating your app:")
print("   app.register_blueprint(auth_bp)")
print("4. Add secret key:")
print("   app.secret_key = 'your-secret-key-123'")
print("5. Add root route redirect:")
print("   @app.route('/')")
print("   def index(): return redirect('/login')")

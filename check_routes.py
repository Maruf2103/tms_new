from flask import Flask
import os

app = Flask(__name__)

# Try to find all route files
route_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and ('route' in file.lower() or 'app' in file.lower() or 'main' in file.lower() or 'init' in file):
            route_files.append(os.path.join(root, file))

print("Found Python files that might contain routes:")
for file in route_files:
    print(f" - {file}")

# Try to import and see routes
try:
    from app import app as flask_app
    print("\n✅ Flask app found in app/__init__.py")
except:
    try:
        from main import app
        print("\n✅ Flask app found in main.py")
    except:
        try:
            from app import app
            print("\n✅ Flask app found in app.py")
        except Exception as e:
            print(f"\n❌ Could not find Flask app: {e}")

print("\nTo see all routes, run: flask routes")

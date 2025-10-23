# auth_integration.py - Add this to your main app
from flask import Flask, redirect

def add_auth_routes(app):
    \"\"\"Add authentication routes to your main Flask app\"\"\"
    
    # Import auth blueprint
    try:
        from app.auth_routes import auth_bp
        app.register_blueprint(auth_bp)
        print(\"✅ Auth blueprint registered successfully\")
    except ImportError as e:
        print(f\"❌ Could not import auth routes: {e}\")
        # Create fallback routes
        @app.route('/login')
        def login_fallback():
            return '''
            <h1>Login Page</h1>
            <form action=\"/login\" method=\"POST\">
                <input type=\"email\" name=\"email\" placeholder=\"Email\" required><br>
                <input type=\"password\" name=\"password\" placeholder=\"Password\" required><br>
                <button type=\"submit\">Login</button>
            </form>
            <a href=\"/signup\">Sign Up</a>
            '''
        
        @app.route('/signup')
        def signup_fallback():
            return '<h1>Sign Up Page</h1><a href=\"/login\">Login</a>'
        
        @app.route('/logout')  
        def logout_fallback():
            return redirect('/login')
        
        print(\"✅ Fallback auth routes created\")
    
    # Add root redirect
    @app.route('/')
    def index():
        return redirect('/login')
    
    return app

# Usage in your main app:
# from auth_integration import add_auth_routes
# app = Flask(__name__)
# app = add_auth_routes(app)

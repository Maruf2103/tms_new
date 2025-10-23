from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1 style="color: green;">✅ SUCCESS! Flask is working!</h1><p>Your TMS can now be developed.</p>'

@app.route('/test')
def test():
    return '<p>Test page is working too!</p>'

@app.route('/login')
def login():
    return '''
    <h2>Login Page</h2>
    <form action="/login" method="POST">
        <input type="email" name="email" placeholder="Email" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p><a href="/">Home</a></p>
    '''

if __name__ == '__main__':
    print("🎯 TEST APP RUNNING ON http://127.0.0.1:5000")
    print("📱 Open your browser and check the URL above")
    print("📍 Available routes:")
    print("   - http://localhost:5000/")
    print("   - http://localhost:5000/test") 
    print("   - http://localhost:5000/login")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>TMS - PORT 8000</title></head>
    <body style="margin: 40px; font-family: Arial;">
        <h1 style="color: green;">✅ WORKING ON PORT 8000!</h1>
        <h2>Your TMS is Ready!</h2>
        <p><strong>If you can see this, development can continue!</strong></p>
        <div style="margin-top: 20px;">
            <a href="/login" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login Page</a>
        </div>
    </body>
    </html>
    '''

@app.route('/login')
def login():
    return '''
    <h2>Login</h2>
    <form action="/login" method="POST">
        <input type="email" name="email" placeholder="Email" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p><a href="/">Home</a></p>
    '''

if __name__ == '__main__':
    print("🚀 STARTING ON PORT 8000...")
    print("📍 VISIT: http://localhost:8000")
    print("📍 VISIT: http://127.0.0.1:8000") 
    print("📍 VISIT: http://192.168.75.67:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)

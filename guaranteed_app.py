from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
    <head><title>TMS Test</title></head>
    <body style="font-family: Arial; margin: 40px;">
        <h1 style="color: green;">🎉 SUCCESS!</h1>
        <h2>Your Flask server is working!</h2>
        <p><strong>URL:</strong> http://localhost:5000</p>
        <p><strong>Next:</strong> You can now develop your TMS application.</p>
        <div style="margin-top: 20px;">
            <a href="/test" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Test Link</a>
        </div>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return '<h2>Test Page</h2><p>This page is also working!</p><a href="/">← Back</a>'

@app.route('/login')
def login():
    return '''
    <h2>Login</h2>
    <form action="/login" method="POST">
        <input type="email" name="email" placeholder="Email" style="padding: 8px; margin: 5px; width: 200px;"><br>
        <input type="password" name="password" placeholder="Password" style="padding: 8px; margin: 5px; width: 200px;"><br>
        <button type="submit" style="padding: 8px 20px; margin: 5px;">Login</button>
    </form>
    <p><a href="/">Home</a></p>
    '''

if __name__ == '__main__':
    print('=' * 50)
    print('🚀 FLASK SERVER STARTING')
    print('=' * 50)
    print('📍 MUST WORK: http://127.0.0.1:5000')
    print('📍 MUST WORK: http://localhost:5000')
    print('📍 Test page: http://localhost:5000/test')
    print('📍 Login page: http://localhost:5000/login')
    print('=' * 50)
    print('If you see this message but browser shows error,')
    print('the issue is with your browser/firewall, not Flask.')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)

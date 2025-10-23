from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return '<h1>🚀 PORT 8080 WORKING!</h1><p>TMS Development Ready</p>'
print("📍 Try: http://localhost:8080")
app.run(host='0.0.0.0', port=8080, debug=True)

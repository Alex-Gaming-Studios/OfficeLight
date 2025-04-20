from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/dashboard')
    return app.send_static_file('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect('/login')
    return app.send_static_file('register.html')

@app.route('/dashboard')
def dashboard():
    return app.send_static_file('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'officelight.db'

# --- Hilfsfunktion ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Startseite mit Ladebildschirm ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Registrierung ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()

        flash('Erfolgreich registriert. Bitte einloggen.')
        return redirect(url_for('login'))

    return render_template('register.html')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Login fehlgeschlagen. Bitte überprüfe deine Eingaben.')

    return render_template('login.html')

# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# --- Einstellungen ---
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        theme = request.form['theme']
        # Update theme in DB, etc.
        flash('Einstellungen aktualisiert.')
    
    return render_template('settings.html')

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('login'))

# --- Lizenzcode Eingabe ---
@app.route('/license', methods=['GET', 'POST'])
def license():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        license_code = request.form['license']
        # Hier kannst du die Lizenzprüfung einbauen (z. B. gegen Datenbank vergleichen)
        flash('Lizenz überprüft.')
        return redirect(url_for('dashboard'))

    return render_template('license.html')

# --- Anwendung starten ---
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Lade deine index.html Seite

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render benötigt Port von Umgebungsvariablen
    app.run(host='0.0.0.0', port=port)
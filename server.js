
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const DB_PATH = './officeLight_database.json';

// Hilfsfunktion zum Laden der Datenbank
function loadDB() {
    const data = fs.readFileSync(DB_PATH);
    return JSON.parse(data);
}

// Hilfsfunktion zum Speichern der Datenbank
function saveDB(db) {
    fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
}

// Registrierung
app.post('/register', (req, res) => {
    const { username, email, password } = req.body;
    const db = loadDB();

    const exists = db.users.find(u => u.email === email);
    if (exists) return res.status(400).json({ message: 'User already exists' });

    const newUser = {
        username,
        email,
        password, // In echter Anwendung: Passwort hashen!
        license: "OfficeLight",
        registered: true
    };

    db.users.push(newUser);
    saveDB(db);
    res.status(201).json({ message: 'User registered successfully' });
});

// Anmeldung
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const db = loadDB();

    const user = db.users.find(u => u.email === email && u.password === password);
    if (!user) return res.status(401).json({ message: 'Invalid credentials' });

    res.status(200).json({ username: user.username, email: user.email, license: user.license });
});

// Lizenz aktivieren
app.post('/activate-license', (req, res) => {
    const { email, code } = req.body;
    const db = loadDB();

    const user = db.users.find(u => u.email === email);
    if (!user) return res.status(404).json({ message: 'User not found' });

    for (const type in db.licenses.available) {
        const index = db.licenses.available[type].indexOf(code);
        if (index !== -1) {
            db.licenses.available[type].splice(index, 1);
            db.licenses.used.push({ code, email });
            user.license = type;
            saveDB(db);
            return res.status(200).json({ message: `License upgraded to ${type}` });
        }
    }

    res.status(400).json({ message: 'Invalid or already used license code' });
});

app.listen(PORT, () => {
    console.log(`OfficeLight backend running at http://localhost:${PORT}`);
});

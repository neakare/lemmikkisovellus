'''Tavoitteena on, että sovelluksessa on ainakin seuraavat toiminnot:
Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
    muuten OK, mutta uloskirjautuminen ei toimi
Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
Käyttäjä näkee sovellukseen lisätyt tietokohteet.
Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.
README.md-tiedoston tulee kuvata, millainen sovellus on ja miten sitä voi testata.
Saat seuraavan viikon alussa ohjaajalta palautteen sovelluksesta Labtooliin.
Vinkkejä palautukseen:
Muista antaa README.md-tiedostossa ohjeet siihen, miten sovelluksen testaaja saa käynnistettyä sovelluksen omalla koneellaan.
Tiedosto database.db ei kuulu repositorioon. Sovelluksen testaajan pitäisi pystyä luomaan tietokanta .sql-tiedostojen perusteella.'''

import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from flask import session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"
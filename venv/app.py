'''Tavoitteena on, että sovelluksessa on ainakin seuraavat toiminnot:
Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
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
from werkzeug.security import generate_password_hash
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

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
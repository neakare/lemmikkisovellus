'''Tavoitteena on, että sovelluksessa on ainakin seuraavat toiminnot:
Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
    muuten OK, mutta ei näytä session kirjautuneen nimeä
Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
    voi lisätä tietokantaan
Käyttäjä näkee sovellukseen lisätyt tietokohteet.
    näkee osoitteella, etusivulla vain silloin kun on kommentti
Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.
    viesteistä voi etsiä
README.md-tiedoston tulee kuvata, millainen sovellus on ja miten sitä voi testata.
Saat seuraavan viikon alussa ohjaajalta palautteen sovelluksesta Labtooliin.
Vinkkejä palautukseen:
Muista antaa README.md-tiedostossa ohjeet siihen, miten sovelluksen testaaja saa käynnistettyä sovelluksen omalla koneellaan.
Tiedosto database.db ei kuulu repositorioon. Sovelluksen testaajan pitäisi pystyä luomaan tietokanta .sql-tiedostojen perusteella.'''

import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
import db, config, users, petinfo

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    pets = petinfo.get_pets()
    return render_template("index.html", pets=pets)

@app.route("/pet/<int:pet_id>")
def show_pet(pet_id):
    pet = petinfo.get_pet(pet_id)
    messages = petinfo.get_messages(pet_id)
    return render_template("pet.html", pet=pet, messages=messages)

@app.route("/new_pet", methods=["POST"])
def new_pet():
    name = request.form["name"]
    species = request.form["species"]
    breed = request.form["breed"]
    user_id = session["user_id"]

    pet_id = petinfo.add_pet(name, species, breed, user_id)
    return redirect("/pet/" + str(pet_id))

@app.route("/new_message", methods=["POST"])
def new_message():
    content = request.form["content"]
    user_id = session["user_id"]
    pet_id = request.form["pet_id"]

    petinfo.add_message(content, user_id, pet_id)
    return redirect("/pet/" + str(pet_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"

        try:
            users.create_user(username, password1)
            return "Tunnus luotu"
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
    
@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query")
    results = petinfo.search(query) if query else []
    return render_template("search.html", query=query, results=results)

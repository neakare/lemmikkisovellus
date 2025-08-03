import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
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
    if not pet:
        abort(404)
    messages = petinfo.get_messages(pet_id)
    return render_template("pet.html", pet=pet, messages=messages)

@app.route("/new_pet", methods=["POST"])
def new_pet():
    require_login()
    name = request.form["name"]
    species = request.form["species"]
    breed = request.form["breed"]
    user_id = session["user_id"]
    if not name or any(len(item) > 100 for item in (name, species, breed)):
        abort(403)
    pet_id = petinfo.add_pet(name, species, breed, user_id)
    return redirect("/pet/" + str(pet_id))

@app.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    require_login()
    pet = petinfo.get_pet(pet_id)
    if not pet:
        abort(404)
    
    if pet["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_pet.html", pet=pet)

    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        breed = request.form["breed"]
        if any(len(item) > 100 for item in (name, species, breed)):
            abort(403)
        petinfo.update_pet(pet_id, name, species, breed)
        return redirect("/pet/" +  str(pet_id))

@app.route("/remove_pet/<int:pet_id>", methods=["GET", "POST"])
def remove_pet(pet_id):
    require_login()
    pet = petinfo.get_pet(pet_id)
    if not pet:
        abort(404)
    
    if pet["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_pet.html", pet=pet)

    if request.method == "POST":
        if "continue" in request.form:
            petinfo.remove_all_messages(pet_id)
            petinfo.remove_pet(pet_id)
        return redirect("/")

@app.route("/new_message", methods=["POST"])
def new_message():
    require_login()
    content = request.form["content"]
    user_id = session["user_id"]
    pet_id = request.form["pet_id"]
    if not content or len(content) > 5000:
        abort(403)
    petinfo.add_message(content, user_id, pet_id)

    return redirect("/pet/" + str(pet_id))

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    require_login()
    message = petinfo.get_message(message_id)
    if not message:
        abort(404)
    
    if message["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", message=message)

    if request.method == "POST":
        content = request.form["content"]
        if len(content) > 5000:
            abort(403)
        petinfo.update_message(message["id"], content)
        return redirect("/pet/" + str(message["pet_id"]))

@app.route("/remove/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    require_login()
    message = petinfo.get_message(message_id)
    if not message:
        abort(404)

    if message["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", message=message)

    if request.method == "POST":
        if "continue" in request.form:
            petinfo.remove_message(message["id"])
        return redirect("/pet/" + str(message["pet_id"]))

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
            return redirect("/login")
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
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
    
@app.route("/logout")
def logout():
    require_login()
    del session["user_id"]
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query")
    results = petinfo.search(query) if query else []
    return render_template("search.html", query=query, results=results)

def require_login():
    if "user_id" not in session:
        abort(403)
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, make_response, flash
import db, config, users, petinfo, secrets, markupsafe
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    pets = petinfo.get_pets()
    activities = petinfo.get_activities()
    appetites = petinfo.get_appetites()
    return render_template("index.html", pets=pets, activities = activities, appetites = appetites)

@app.route("/pet/<int:pet_id>")
def show_pet(pet_id):
    pet = petinfo.get_pet(pet_id)
    if not pet:
        abort(404)
    messages = petinfo.get_messages(pet_id)
    grades = petinfo.get_grades(pet_id)
    grade_statistics = petinfo.get_grade_statistics(pet_id)
    user_id = session.get("user_id")
    grade = None
    is_graded = False

    if user_id:
        grade = petinfo.get_grade(pet_id, user_id)
        if grade:
            is_graded = True

    return render_template("pet.html", pet=pet, messages=messages, grades=grades, grade_statistics=grade_statistics, is_graded=is_graded, grade=grade)

@app.route("/new_pet", methods=["POST"])
def new_pet():
    require_login()
    check_csrf()

    name = request.form["name"]
    species = request.form["species"]
    breed = request.form["breed"]
    user_id = session["user_id"]
    activity_id = request.form["activity"]
    appetite_id = request.form["appetite"]

    if not name or any(len(item) > 100 for item in (name, species, breed)):
        abort(403)
    
    if not species:
        abort(404)

    if not activity_id:
        abort(404)
        
    if not appetite_id:
        abort(404)
        
    pet_id = petinfo.add_pet(name, species, breed, user_id, activity_id, appetite_id)
    return redirect("/pet/" + str(pet_id))

@app.route("/edit_pet/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    require_login()
    pet = petinfo.get_pet(pet_id)
    activities = petinfo.get_activities()
    appetites = petinfo.get_appetites()

    if not pet:
        abort(404)
    
    if pet["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_pet.html", pet=pet, activities = activities, appetites = appetites)

    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        breed = request.form["breed"]
        activity_id = request.form["activity"]
        appetite_id = request.form["appetite"]

        if any(len(item) > 40 for item in (name, species, breed, activity_id, appetite_id)):
            abort(403)
        
        if not species:
            abort(404)
        
        if not name:
            abort(404)

        if not activity_id:
            abort(404)
        
        if not appetite_id:
            abort(404)

        check_csrf()
        petinfo.update_pet(pet_id, name, species, breed, activity_id, appetite_id)
        flash("Tietojen päivittäminen onnistui")
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
            check_csrf()
            petinfo.remove_all_messages(pet_id)
            petinfo.remove_all_grades(pet_id)
            petinfo.remove_pet(pet_id)
            flash("Lemmikin poistaminen onnistui")
        elif "cancel" in request.form:
            return redirect ("/pet/" +  str(pet_id))
        return redirect("/")
    
@app.route("/pet/add_image/<int:pet_id>", methods=["GET", "POST"])
def add_image_pet(pet_id):
    require_login()
    pet = petinfo.get_pet(pet_id)
    if pet["user_id"] != session["user_id"]:
            abort(403)

    if request.method == "GET":
        return render_template("add_image_pet.html", pet=pet)

    if request.method == "POST":
        if "continue" in request.form:
            file = request.files["image"]

            if not file.filename.endswith(".jpg"):
                flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
                return redirect("/pet/add_image/" + str(pet_id))

            image = file.read()
            if len(image) > 100 * 1024:
                flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
                return redirect("/pet/add_image/" + str(pet_id))
            
            check_csrf()
            petinfo.update_image(image, pet_id)
            flash("Kuvan lisääminen onnistui")
        
        return redirect("/pet/" + str(pet_id))

@app.route("/image_pet/<int:pet_id>")
def show_image_pet(pet_id):
    image = petinfo.get_image(pet_id)

    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response
    
@app.route("/remove/image_pet/<int:pet_id>", methods=["GET", "POST"])
def remove_image_pet(pet_id):
    require_login()
    pet = petinfo.get_pet(pet_id)
    image = petinfo.get_image(pet_id)

    if not image:
        abort(404)
    
    if pet["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_pet_image.html", pet=pet)

    if request.method == "POST":
        if "continue" in request.form:
            check_csrf()
            petinfo.remove_image(pet_id)
            flash("Kuvan poistaminen onnistui")
        
        return redirect ("/pet/" +  str(pet_id))

@app.route("/new_message", methods=["POST"])
def new_message():
    require_login()
    check_csrf()
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
    pet = petinfo.get_pet(message["pet_id"])
    if not message:
        abort(404)
    
    if message["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", message=message, pet=pet)

    if request.method == "POST":
        if "continue" in request.form:
            content = request.form["content"]
            if len(content) >=0 and len (content)> 5000:
                abort(403)
            check_csrf()
            petinfo.update_message(message["id"], content)
            flash("Kommentin päivittäminen onnistui")
            return redirect("/pet/" + str(message["pet_id"]))
    
        elif "cancel" in request.form:
                return redirect ("/pet/" + str(message["pet_id"]))

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
            check_csrf()
            petinfo.remove_message(message["id"])
            flash("Kommentin poistaminen onnistui")
        return redirect("/pet/" + str(message["pet_id"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2: 
            flash("VIRHE: Antamasi salasanat eivät ole samat") 
            filled = {"username": username} 
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1)
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
            return redirect("/login")
        
        except: 
            flash("VIRHE: Valitsemasi tunnus on jo varattu")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            flash("Sisäänkirjautuminen onnistui")
            if urlparse(next_page).path == "/register": #user is redirected to the frontpage, if they have been on the register-page before login.
                return redirect ("/")
            else:
                return redirect(next_page)
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return render_template("login.html", next_page=next_page)
    
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

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    messages = users.get_messages(user_id)
    pets = users.get_pets(user_id)
    return render_template("user.html", user=user, messages=messages, pets=pets)

@app.route("/add_image_user", methods=["GET", "POST"])
def add_image_user():
    require_login()
    user = users.get_user(session["user_id"])

    if request.method == "GET":
        return render_template("add_image_user.html", user=user)

    if request.method == "POST":
        user_id = session["user_id"]
        check_csrf()
        if "continue" in request.form:
            file = request.files["image"]
            if not file.filename.endswith(".jpg"):
                flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
                return redirect ("/add_image_user")

            image = file.read()
            if len(image) > 100 * 1024:
                flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
                return redirect ("/add_image_user")

            users.update_image(user_id, image)
            flash("Kuvan lisääminen onnistui")
        
        return redirect("/user/" + str(user_id))

@app.route("/image_user/<int:user_id>")
def show_image_user(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/remove/image_user/<int:user_id>", methods=["GET", "POST"])
def remove_image_user(user_id):
    require_login()
    image = users.get_image(user_id)
    user_id = session["user_id"]
    user = users.get_user(user_id)

    if not image:
        abort(404)
    
    if user_id != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_user_image.html", user=user)
    
    if request.method == "POST":
        check_csrf()

        if "cancel" in request.form:
            return redirect("/user/" + str(user_id))
        
        if "continue" in request.form:
            users.remove_image(user_id)
            flash("Kuvan poistaminen onnistui")
            return redirect("/user/" + str(user_id))
    

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/new_grade", methods=["POST"])
def new_grade():
    require_login()
    check_csrf()
    grade = request.form["grade"]
    user_id = session["user_id"]
    pet_id = request.form["pet_id"]

    if not grade:
        abort(403)
    
    if not grade.isnumeric():
        flash("Arvosanan tulee olla välillä 1-5")
        return redirect("/pet/" + str(pet_id))
    
    if petinfo.get_grade(pet_id, user_id):
        flash("Olet jo arvostellut tämän lemmikin.")
        return redirect("/pet/" + str(pet_id))
    
    if "grade" in request.form:
            petinfo.add_grade(grade, user_id, pet_id)
            flash("Arvostelun lisääminen onnistui")
            return redirect("/pet/" + str(pet_id))

@app.route("/edit_grade/<int:grade_id>", methods=["GET", "POST"])
def edit_grade(grade_id):
    require_login()
    grade = petinfo.get_grade_id(grade_id)
    pet = petinfo.get_pet(grade["pet_id"])

    if not grade:
        abort(404)
    
    if grade["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_grade.html", pet=pet, grade=grade)

    if request.method == "POST":
        newgrade = request.form["grade"]
        check_csrf()
        petinfo.update_grade(grade["id"], newgrade)
        flash("Arvostelun päivittäminen onnistui")
        return redirect("/pet/" + str(grade["pet_id"]))
    
@app.route("/remove_grade/<int:grade_id>", methods=["GET", "POST"])
def remove_grade(grade_id):
    require_login()
    grade = petinfo.get_grade_id(grade_id)
    pet = petinfo.get_pet(grade["pet_id"])

    if not grade:
        abort(404)

    if grade["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_grade.html", grade=grade, pet=pet)

    if request.method == "POST":
        if "continue" in request.form:
            check_csrf()
            petinfo.remove_grade(grade["id"])
            flash("Arvostelun poistaminen onnistui")
        return redirect("/pet/" + str(grade["pet_id"]))
    
import os


from bson.objectid import ObjectId
from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)
from flask_pymongo import PyMongo
import json
import requests
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    if session.get("user") is None:
        return render_template("home.html")
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        return render_template("home.html", username=username)


@app.errorhandler(404)
def invalid_route(e):
    if session.get("user") is None:
        return render_template("error/404.html")
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    return render_template("error/404.html", username=username)


@app.route("/circuits")
def circuits():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    circuits = list(mongo.db.circuits.find())
    return render_template('circuits.html',
                           circuits=circuits,
                           username=username
                           )


@app.route("/constructors")
def constructors():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    constructors = list(mongo.db.constructors.find())
    return render_template('constructors.html',
                           constructors=constructors,
                           username=username
                           )


@app.route("/drivers")
def drivers():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    drivers = list(mongo.db.drivers.find())
    return render_template('drivers.html',
                           drivers=drivers,
                           username=username
                           )


@app.route("/edit_driver/<driver_id>", methods=["GET", "POST"])
def edit_driver(driver_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    if request.method == "POST":
        submit = {
            "forename": request.form.get("forename"),
            "surname": request.form.get("surname"),
            "number": request.form.get("number"),
            "code": request.form.get("code"),
            "nationality": request.form.get("nationality"),
            "dob": request.form.get("dob"),
            "url": request.form.get("url"),
            "driverId": int(request.form.get("driverId")),
            "driverRef": request.form.get("driverRef"),
        }
        mongo.db.drivers.replace_one({"_id": ObjectId(driver_id)}, submit)
    drivers = mongo.db.drivers.find_one({"_id": ObjectId(driver_id)})
    countries = list(mongo.db.countries.find().sort("nationality", 1))
    return render_template("edit/edit_driver.html",
                           countries=countries,
                           drivers=drivers,
                           username=username)


@app.route("/edit_race/<race_id>", methods=["GET", "POST"])
def edit_race(race_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    races = mongo.db.races.find_one({"_id": ObjectId(race_id)})
    results = list(mongo.db.results.find(
        {"raceId": races["raceId"]}).sort("positionOrder", 1))
    statuses = list(mongo.db.status.find().sort("status", 1))
    drivers = list(mongo.db.drivers.find())
    seasons = list(mongo.db.seasons.find())
    driver_standings = list(mongo.db.driver_standings.find(
        {"raceId": races["raceId"]}).sort("position", 1))
    circuits = list(mongo.db.circuits.find())
    qualifying = list(mongo.db.qualifying.find(
        {"raceId": races["raceId"]}).sort("position", 1))
    constructors = list(mongo.db.constructors.find())
    constructor_standings = list(mongo.db.constructor_standings.find(
        {"raceId": races["raceId"]}).sort("position", 1))
    previous_race = list(mongo.db.races.find(
        {"year": races["year"], "round": races["round"] - 1}))

    if request.method == "POST":

        if request.form["action"] == "qualifying":
            for n in range(20):
                qualifying = {
                    "raceId": races["raceId"],
                    "driverId": int(request.form.get(
                        "driver_id_pos_quali_" + str(n))),
                    "constructorId": int(request.form.get(
                        "constructor_id_quali_pos_" + str(n))),
                    "position": n+1,
                    "q1": request.form.get("q1_pos_" + str(n)),
                    "q2": request.form.get("q2_pos_" + str(n)),
                    "q3": request.form.get("q3_pos_" + str(n)),
                }
                mongo.db.qualifying.insert_one(qualifying)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "qualifying-update":
            for n in range(20):
                qualifying_update = {
                    "raceId": races["raceId"],
                    "driverId": int(request.form.get(
                        "driver_id_pos_quali_" + str(n))),
                    "constructorId": int(request.form.get(
                        "constructor_id_quali_pos_" + str(n))),
                    "position": n+1,
                    "q1": request.form.get("q1_pos_" + str(n)),
                    "q2": request.form.get("q2_pos_" + str(n)),
                    "q3": request.form.get("q3_pos_" + str(n)),
                }
                mongo.db.qualifying.replace_one(
                    {"raceId": races["raceId"], "position": n+1},
                    qualifying_update)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "race":
            for n in range(20):
                race = {
                    "raceId": races["raceId"],
                    "driverId": int(request.form.get(
                        "driver_id_pos_race_" + str(n))),
                    "constructorId": int(request.form.get(
                        "constructor_id_race_pos_" + str(n))),
                    "position": int(request.form.get(
                        "position_pos_" + str(n))),
                    "positionText": request.form.get(
                        "position_text_pos_" + str(n)),
                    "positionOrder": n+1,
                    "points": int(request.form.get(
                        "points_pos_race_" + str(n))),
                    "laps": int(request.form.get(
                        "laps_pos_race_" + str(n))),
                    "statusId": int(request.form.get(
                        "status_id_pos_race_" + str(n))),
                }
                mongo.db.results.insert_one(race)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "race-update":
            for n in range(20):
                race_update = {
                    "raceId": races["raceId"],
                    "driverId": int(request.form.get(
                        "driver_id_pos_race_" + str(n))),
                    "constructorId": int(request.form.get(
                        "constructor_id_race_pos_" + str(n))),
                    "position": request.form.get(
                        "position_pos_" + str(n)),
                    "positionText": request.form.get(
                        "position_text_pos_" + str(n)),
                    "positionOrder": n+1,
                    "points": int(request.form.get(
                        "points_pos_race_" + str(n))),
                    "laps": int(request.form.get(
                        "laps_pos_race_" + str(n))),
                    "statusId": int(request.form.get(
                        "status_id_pos_race_" + str(n))),
                }
                print(race_update)
                mongo.db.results.replace_one(
                    {"raceId": races["raceId"], "positionOrder": n+1},
                    race_update)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "driver":
            for n in range(20):
                driver_standings = {
                    "raceId": races["raceId"],
                    "driverId": int(request.form.get(
                        "driver_id_standings_pos_" + str(n))),
                    "points": int(request.form.get(
                        "points_standings_pos_" + str(n))),
                    "position": n+1,
                    "positionText": n+1,
                    "wins": int(request.form.get(
                        "wins_standings_pos_" + str(n))),
                }
                mongo.db.driver_standings.insert_one(driver_standings)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "driver-update":
            for n in range(20):
                driver_standings_update = {
                    "raceId": races["raceId"],
                    "driverId": int(request.form.get(
                        "driver_id_standings_pos_" + str(n))),
                    "points": int(request.form.get(
                        "points_standings_pos_" + str(n))),
                    "position": n+1,
                    "positionText": n+1,
                    "wins": int(request.form.get(
                        "wins_standings_pos_" + str(n))),
                }
                mongo.db.driver_standings.replace_one(
                    {"raceId": races["raceId"], "position": n+1},
                    driver_standings_update)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "constructor":
            for n in range(10):
                constructor_standings = {
                    "raceId": races["raceId"],
                    "constructorId": int(request.form.get(
                        "constructor_id_standings_pos_" + str(n))),
                    "points": int(request.form.get(
                        "points_constructor_pos_" + str(n))),
                    "position": n+1,
                    "positionText": n+1,
                    "wins": int(request.form.get(
                        "wins_constructor_pos_" + str(n))),
                }
                mongo.db.constructor_standings.insert_one(
                    constructor_standings)
            return redirect(url_for("view_race", race_id=races["_id"]))

        elif request.form["action"] == "constructor-update":
            for n in range(10):
                constructor_standings_update = {
                    "raceId": races["raceId"],
                    "constructorId": int(request.form.get(
                        "constructor_id_standings_pos_" + str(n))),
                    "points": int(request.form.get(
                        "points_constructor_pos_" + str(n))),
                    "position": n+1,
                    "positionText": n+1,
                    "wins": int(request.form.get(
                        "wins_constructor_pos_" + str(n))),
                }

                mongo.db.constructor_standings.replace_one(
                    {"raceId": races["raceId"], "position": n+1},
                    constructor_standings_update)
            return redirect(url_for("view_race", race_id=races["_id"]))
        else:
            return redirect(url_for("home"))

    return render_template(
        "edit/edit_race.html",
        statuses=statuses,
        races=races,
        results=results,
        drivers=drivers,
        constructors=constructors,
        qualifying=qualifying,
        circuits=circuits,
        driver_standings=driver_standings,
        constructor_standings=constructor_standings,
        seasons=seasons,
        previous_race=previous_race,
        username=username)


@app.route("/races")
def races():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    races = list(mongo.db.races.find().sort("year", 1))
    seasons = list(mongo.db.seasons.find())
    circuits = list(mongo.db.circuits.find())
    return render_template('races.html',
                           races=races,
                           seasons=seasons,
                           circuits=circuits,
                           username=username
                           )


@app.route("/seasons")
def seasons():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    seasons = list(mongo.db.seasons.find())
    return render_template('seasons.html',
                           seasons=seasons,
                           username=username
                           )


@app.route("/view_circuit/<circuit_id>", methods=["GET", "POST"])
def view_circuit(circuit_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    circuits = mongo.db.circuits.find_one(
        {"_id": ObjectId(circuit_id)})
    races = list(mongo.db.races.find().sort("year", 1))
    seasons = list(mongo.db.seasons.find().sort("year", 1))
    favourites = list(mongo.db.favourites.find(
        {"username": username} and {"circuitId": ObjectId(circuit_id)}))
    if request.method == "POST":
        if request.form["action"] == "add":
            circuit = {
                "username": username,
                "circuitId": circuits["_id"],
                }
            mongo.db.favourites.insert_one(circuit)
        elif request.form["action"] == "remove":
            mongo.db.favourites.delete_one({"circuitId": circuits["_id"]})
        return redirect(url_for("view_circuit", circuit_id=circuits["_id"]))
    return render_template(
        "view/view_circuit.html",
        races=races,
        circuits=circuits,
        seasons=seasons,
        username=username,
        favourites=favourites)


@app.route("/view_constructor/<constructor_id>", methods=["GET", "POST"])
def view_constructor(constructor_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    constructors = mongo.db.constructors.find_one(
        {"_id": ObjectId(constructor_id)})
    constructor_results = list(mongo.db.results.find(
        {"constructorId": constructors["constructorId"]}))
    wins = list(mongo.db.results.find(
        {"constructorId": constructors["constructorId"], "position": 1}))
    second = list(mongo.db.results.find(
        {"constructorId": constructors["constructorId"], "position": 2}))
    third = list(mongo.db.results.find(
        {"constructorId": constructors["constructorId"], "position": 3}))
    favourites = list(mongo.db.favourites.find(
        {"username": username} and
        {"constructorId": ObjectId(constructor_id)}))
    if request.method == "POST":
        if request.form["action"] == "add":
            constructor = {
                "username": username,
                "constructorId": constructors["_id"],
                }
            mongo.db.favourites.insert_one(constructor)
        elif request.form["action"] == "remove":
            mongo.db.favourites.delete_one(
                {"constructorId": constructors["_id"]})
        return redirect(url_for("view_constructor",
                                constructor_id=constructors["_id"]))

    def get_wiki_main_image(title):
        url = 'https://en.wikipedia.org/w/api.php'
        data = {
            'action': 'query',
            'format': 'json',
            'formatversion': 2,
            'prop': 'pageimages|pageterms',
            'piprop': 'original',
            'titles': title
        }
        response = requests.get(url, data)
        json_data = json.loads(response.text)
        return json_data['query']['pages'][0]['original']['source'] if len(
            json_data['query']['pages']) > 0 else 'Not found'
    try:
        image = get_wiki_main_image(constructors["name"])
    except KeyError:
        image = "../static/img/no_image_available.svg"
    return render_template(
        "view/view_constructor.html",
        results=constructor_results,
        constructors=constructors,
        wins=wins, second=second,
        third=third,
        username=username,
        image=image,
        favourites=favourites)


@app.route("/view_driver/<driver_id>", methods=["GET", "POST"])
def view_driver(driver_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    drivers = mongo.db.drivers.find_one(
        {"_id": ObjectId(driver_id)})
    results = list(mongo.db.results.find(
        {"driverId": drivers["driverId"]}))
    wins = list(mongo.db.results.find(
        {"driverId": drivers["driverId"], "position": 1}))
    second = list(mongo.db.results.find(
        {"driverId": drivers["driverId"], "position": 2}))
    third = list(mongo.db.results.find(
        {"driverId": drivers["driverId"], "position": 3}))
    favourites = list(mongo.db.favourites.find(
            {"username": username} and {"driverId": ObjectId(driver_id)}))
    did_not_finish = list(mongo.db.results.find(
        {"driverId": drivers["driverId"], "position": ""}))
    hide_chart = (did_not_finish == results)
    if request.method == "POST":
        if request.form["action"] == "add":
            driver = {
                "username": username,
                "driverId": drivers["_id"],
                }
            mongo.db.favourites.insert_one(driver)
        elif request.form["action"] == "remove":
            mongo.db.favourites.delete_one({"driverId": drivers["_id"]})
        return redirect(url_for("view_driver", driver_id=drivers["_id"]))

    # https://stackoverflow.com/questions/59801085/
    # finding-the-main-picture-of-the-wikipedia-page-with-python
    def get_wiki_main_image(title):
        url = 'https://en.wikipedia.org/w/api.php'
        data = {
            'action': 'query',
            'format': 'json',
            'formatversion': 2,
            'prop': 'pageimages|pageterms',
            'piprop': 'original',
            'titles': title
        }
        response = requests.get(url, data)
        json_data = json.loads(response.text)
        return json_data['query']['pages'][0]['original']['source'] if len(
            json_data['query']['pages']) > 0 else 'Not found'
    try:
        image = get_wiki_main_image(
            drivers["forename"] + " " + drivers["surname"])
    except KeyError:
        image = "../static/img/no_image_available.svg"
    return render_template(
        "view/view_driver.html",
        results=results,
        drivers=drivers,
        wins=wins,
        second=second,
        third=third,
        username=username,
        image=image,
        favourites=favourites,
        all_finishes=did_not_finish,
        hide_chart=hide_chart)


@app.route("/view_race/<race_id>", methods=["GET", "POST"])
def view_race(race_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    races = mongo.db.races.find_one({"_id": ObjectId(race_id)})
    statuses = list(mongo.db.status.find())
    drivers = list(mongo.db.drivers.find())
    seasons = list(mongo.db.seasons.find())
    driver_standings = list(mongo.db.driver_standings.find(
        {"raceId": races["raceId"]}).sort("position", 1))
    circuits = list(mongo.db.circuits.find())
    qualifying = list(mongo.db.qualifying.find(
        {"raceId": races["raceId"]}).sort("position", 1))
    constructors = list(mongo.db.constructors.find())
    constructor_standings = list(mongo.db.constructor_standings.find(
        {"raceId": races["raceId"]}).sort("position", 1))
    results = list(mongo.db.results.find().sort("positionOrder", 1))
    favourites = list(mongo.db.favourites.find({"username": username} and
                                               {"raceId": ObjectId(race_id)}))
    if request.method == "POST":
        if request.form["action"] == "add":
            race = {
                "username": username,
                "raceId": races["_id"],
                }
            mongo.db.favourites.insert_one(race)
        elif request.form["action"] == "remove":
            mongo.db.favourites.delete_one({"raceId": races["_id"]})
        return redirect(url_for("view_race", race_id=races["_id"]))
    return render_template(
        "view/view_race.html",
        statuses=statuses,
        races=races,
        results=results,
        drivers=drivers,
        constructors=constructors,
        qualifying=qualifying,
        circuits=circuits,
        driver_standings=driver_standings,
        constructor_standings=constructor_standings,
        seasons=seasons,
        username=username,
        favourites=favourites)


@app.route("/view_season/<season_id>")
def view_season(season_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    seasons = mongo.db.seasons.find_one({"_id": ObjectId(season_id)})
    races = list(mongo.db.races.find().sort("round", 1))
    constructors = list(mongo.db.constructors.find(
        {"constructorId": seasons["constructorChampionId"]}))
    circuits = list(mongo.db.circuits.find())
    drivers = list(mongo.db.drivers.find(
        {"driverId": seasons["driverChampionId"]}))
    return render_template(
        "view/view_season.html",
        races=races,
        seasons=seasons,
        constructors=constructors,
        drivers=drivers,
        circuits=circuits,
        username=username)


# AUTH ROUTES

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "display_name": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out.")
    session.pop("user")
    return redirect(url_for("login"))

# PROFILE ROUTES


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    if session.get("user") is None:
        return render_template("home.html")
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    display_name = mongo.db.users.find_one(
        {"username": session["user"]})["display_name"]

    if request.method == "POST":
        # update display name
        mongo.db.users.update_one(
            {"username": session["user"]},
            {"$set": {"display_name": request.form.get("display_name")}}
        )
        flash("Display name updated")
        return redirect(url_for("profile", username=session["user"]))

    if session["user"]:
        return render_template("profile/profile.html",
                               username=username,
                               display_name=display_name)

    return redirect(url_for("login"))


@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})
    if request.method == "POST":
        if check_password_hash(
                username["password"], request.form.get("currentPassword")):
                mongo.db.users.update_one(
                    {"username": session["user"]},
                    {"$set": {"password": generate_password_hash(
                        request.form.get("newPassword"))}})
                flash("Password has been updated successfully.")
                return redirect(url_for("profile", username=session["user"]))
        else:
            flash("Incorrect Password")
            return redirect(url_for("change_password",
                                    username=session["user"]))

    return render_template("profile/change_password.html", username=username)


@app.route("/deleteaccount", methods=["GET", "POST"])
def delete_account():

    if session.get("user") is None:
            return redirect(url_for("home"))
    else:
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]

    if request.method == "POST":
            # check if username matches
            user_to_be_deleted = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if user_to_be_deleted["username"] == username.lower():
                mongo.db.users.delete_one({"username": username})
                flash("Account has been deleted.")
                session.pop("user")
                return redirect(url_for("login"))
            else:
                flash("Username does not match.")
                return redirect(url_for("delete_account"))
    return render_template("profile/delete_account.html", username=username)


@app.route("/favourites", methods=["GET", "POST"])
def favourites():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        display_name = mongo.db.users.find_one(
            {"username": session["user"]})["display_name"]
        favourites = list(mongo.db.favourites.find())
        circuits = list(mongo.db.circuits.find())
        constructors = list(mongo.db.constructors.find())
        drivers = list(mongo.db.drivers.find())
        races = list(mongo.db.races.find())

        if request.method == "POST":
            if request.form["action"] == "circuit":
                mongo.db.favourites.delete_one(
                    {"circuitId": circuits["_id"]})
            elif request.form["action"] == "constructor":
                mongo.db.favourites.delete_one(
                    {"constructorId": constructors["_id"]})
            elif request.form["action"] == "driver":
                mongo.db.favourites.delete_one(
                    {"driverId": drivers["_id"]})
            elif request.form["action"] == "race":
                mongo.db.favourites.delete_one(
                    {"raceId": races["_id"]})
            return redirect(url_for("favourites"))
    return render_template("profile/favourites.html",
                           username=username,
                           display_name=display_name,
                           favourites=favourites,
                           circuits=circuits,
                           constructors=constructors,
                           drivers=drivers,
                           races=races)

# Admin Routes


@app.route("/dashboard")
def dashboard():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    if username == "admin":
        return render_template("admin/dashboard.html", username=username)
    else:
        return redirect(url_for("login"))


@app.route("/add_circuit", methods=["GET", "POST"])
def add_circuit():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    if request.method == "POST":
            circuit = {
                "circuitId": int(request.form.get("circuitId")),
                "circuitRef": request.form.get("circuitRef"),
                "name": request.form.get("circuitName"),
                "location": request.form.get("location"),
                "country": request.form.get("country"),
                "lat": float(request.form.get("latitude")),
                "lng": float(request.form.get("longitude")),
                "url": request.form.get("url"),
                }
            mongo.db.circuits.insert_one(circuit)
            flash("Circuit has been added.")
            return redirect(url_for("dashboard"))
    if username == "admin":
        circuits = mongo.db.circuits.find_one(sort=[("circuitId", -1)])
        return render_template("admin/add_circuit.html",
                               username=username,
                               circuits=circuits)
    else:
        return redirect(url_for("login"))


@app.route("/add_constructor", methods=["GET", "POST"])
def add_constructor():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    countries = list(mongo.db.countries.find().sort("nationality", 1))
    if request.method == "POST":
            constructor = {
                "constructorId": int(request.form.get("constructorId")),
                "constructorRef": request.form.get("constructorRef"),
                "name": request.form.get("constructorName"),
                "nationality": request.form.get("nationality"),
                "url": request.form.get("url"),
                }
            mongo.db.constructors.insert_one(constructor)
            flash("Constructor has been added.")
            return redirect(url_for("dashboard"))
    if username == "admin":
        constructors = mongo.db.constructors.find_one(
            sort=[("constructorId", -1)])
        return render_template("admin/add_constructor.html",
                               username=username,
                               constructors=constructors,
                               countries=countries)
    else:
        return redirect(url_for("login"))


@app.route("/add_driver", methods=["GET", "POST"])
def add_driver():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    countries = list(mongo.db.countries.find().sort("nationality", 1))
    if request.method == "POST":
            driver = {
                "driverId": int(request.form.get("driverId")),
                "driverRef": request.form.get("driverRef"),
                "number": request.form.get("number"),
                "code": request.form.get("code"),
                "forename": request.form.get("forename"),
                "surname": request.form.get("forename"),
                "dob": request.form.get("dob"),
                "nationality": request.form.get("nationality"),
                "url": request.form.get("url"),
                }
            mongo.db.drivers.insert_one(driver)
            flash("Driver has been added.")
            return redirect(url_for("dashboard"))
    if username == "admin":
        drivers = mongo.db.drivers.find_one(sort=[("driverId", -1)])
        return render_template("admin/add_driver.html",
                               username=username,
                               drivers=drivers,
                               countries=countries)
    else:
        return redirect(url_for("login"))


@app.route("/add_race", methods=["GET", "POST"])
def add_race():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    if request.method == "POST":
            race = {
                "raceId": int(request.form.get("raceId")),
                "year": int(request.form.get("year")),
                "round": int(request.form.get("round")),
                "circuitId": int(request.form.get("circuitId")),
                "name": request.form.get("name"),
                "date": request.form.get("date"),
                "time": request.form.get("time"),
                "url": request.form.get("url"),
                }
            mongo.db.races.insert_one(race)
            flash("Race has been added.")
            return redirect(url_for("dashboard"))
    if username == "admin":
        races = mongo.db.races.find_one(sort=[("raceId", -1)])
        circuits = list(mongo.db.circuits.find())
        return render_template("admin/add_race.html",
                               username=username,
                               races=races,
                               circuits=circuits)
    else:
        return redirect(url_for("login"))


@app.route("/add_season", methods=["GET", "POST"])
def add_season():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        drivers = list(mongo.db.drivers.find())
        constructors = list(mongo.db.constructors.find())
    if request.method == "POST":
        if mongo.db.seasons.find_one(
                {"year": int(request.form.get("year"))}) is None:
            season = {
                "year": int(request.form.get("year")),
                "no_of_races": int(request.form.get(
                    "no_of_races")),
                "driverChampionId": request.form.get(
                    "driverChampionId"),
                "constructorChampionId": request.form.get(
                    "constructorChampionId"),
                "url": request.form.get("url"),
                }
            mongo.db.seasons.insert_one(season)
            flash("Season has been added.")
            return redirect(url_for("dashboard"))
        else:
            flash("Season already exists.")
            return redirect(url_for("dashboard"))
    if username == "admin":
        return render_template("admin/add_season.html",
                               username=username,
                               drivers=drivers,
                               constructors=constructors)
    else:
        return redirect(url_for("login"))


@app.route("/manage_users")
def manage_users():
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        users = list(mongo.db.users.find({"username": {"$ne": "admin"}}))
    if username == "admin":
        return render_template("admin/manage_users.html",
                               username=username,
                               users=users)
    else:
        return redirect(url_for("login"))


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        users = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": users["username"]},
                {"$set": {"display_name": request.form.get("display_name")}})
            flash("Display Name has been updated successfully.")
            return redirect(url_for("manage_users"))
    if username == "admin":
        return render_template("admin/edit_user.html",
                               username=username,
                               users=users)
    else:
        return redirect(url_for("login"))


@app.route("/delete_user/<user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    if session.get("user") is None:
        return redirect(url_for("home"))
    else:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        users = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        if request.method == "POST":
                mongo.db.users.delete_one({"username": users["username"]})
                flash("Account has been deleted.")
                return redirect(url_for("manage_users"))
    if username == "admin":
        return render_template("admin/delete_user.html",
                               username=username,
                               users=users)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

from calendar import c
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
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("error/404.html", username=username)


@app.route("/circuits")
def circuits():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    circuits = list(mongo.db.circuits.find())
    return render_template('circuits.html',
                           circuits=circuits,
                           username=username
                           )


@app.route("/constructors")
def constructors():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    constructors = list(mongo.db.constructors.find())
    return render_template('constructors.html',
                           constructors=constructors,
                           username=username
                           )

@app.route("/dashboard")
def dashboard():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if username == "admin":
        return render_template("dashboard.html", username=username)
    else: 
         return redirect(url_for("login"))


@app.route("/drivers")
def drivers():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    drivers = list(mongo.db.drivers.find())
    return render_template('drivers.html',
                           drivers=drivers,
                           username=username
                           )

@app.route("/edit_driver/<driver_id>", methods=["GET", "POST"])
def edit_driver(driver_id):
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
            "driverId": request.form.get("driverId"),
            "driverRef": request.form.get("driverRef"),
        }
        mongo.db.drivers.replace_one({"_id": ObjectId(driver_id)}, submit)

    drivers = mongo.db.drivers.find_one({"_id": ObjectId(driver_id)})
    countries = list(mongo.db.countries.find().sort("nationality", 1))
    return render_template("edit/edit_driver.html", countries=countries, drivers=drivers, username=username)

@app.route("/edit_race/<race_id>", methods=["GET", "POST"])
def edit_race(race_id):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    races = mongo.db.races.find_one({"_id": ObjectId(race_id)})
    results = list(mongo.db.results.find({"raceId": races["raceId"]}).sort("positionOrder", 1))
    statuses = list(mongo.db.status.find().sort("status", 1))
    drivers = list(mongo.db.drivers.find())
    seasons = list(mongo.db.seasons.find())
    driver_standings = list(mongo.db.driver_standings.find({"raceId": races["raceId"]}).sort("position", 1))
    circuits = list(mongo.db.circuits.find())
    qualifying = list(mongo.db.qualifying.find({"raceId": races["raceId"]}).sort("position", 1))
    constructors = list(mongo.db.constructors.find())
    constructor_standings = list(mongo.db.constructor_standings.find({"raceId": races["raceId"]}).sort("position", 1))
    previous_race = list(mongo.db.races.find({"year": races["year"], "round": races["round"] - 1}))
    
    if request.method == "POST":
        print(races)
        for n in range(20):
            qualifying = {
                "raceId": races["raceId"],
                "driverId": request.form.get("driver_id_pos_quali_" + str(n)),
                "constructorId": request.form.get("constructor_id_quali_pos_" + str(n)),
                "position": n+1,
                "q1": request.form.get("q1_pos_" + str(n)),
                "q2": request.form.get("q2_pos_" + str(n)),
                "q3": request.form.get("q3_pos_" + str(n)),
            }
            mongo.db.test.insert_one(qualifying)
    return render_template(
        "edit/edit_race.html", statuses=statuses, races=races, results=results, drivers=drivers, constructors=constructors, qualifying=qualifying, 
        circuits=circuits, driver_standings=driver_standings, constructor_standings=constructor_standings, seasons=seasons, previous_race=previous_race,
        username=username)

@app.route("/races")
def races():
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
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    seasons = list(mongo.db.seasons.find())
    return render_template('seasons.html',
                           seasons=seasons,
                           username=username
                           )


@app.route("/view_circuit/<circuit_id>")
def view_circuit(circuit_id):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    circuits = mongo.db.circuits.find_one({"_id": ObjectId(circuit_id)})
    races = list(mongo.db.races.find().sort("year", 1))
    seasons = list(mongo.db.seasons.find().sort("year", 1))
    print(seasons)
    return render_template(
        "view/view_circuit.html", races=races, circuits=circuits, seasons=seasons, username=username)

@app.route("/view_constructor/<constructor_id>")
def view_constructor(constructor_id):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    constructors = mongo.db.constructors.find_one({"_id": ObjectId(constructor_id)})
    constructor_results = list(mongo.db.constructor_results.find({"constructorId": constructors["constructorId"]}))
    seasons = list(mongo.db.seasons.find({"constructorChampionId": constructors["constructorId"]})) 
    return render_template(
        "view/view_constructor.html", constructor_results=constructor_results, constructors=constructors, seasons=seasons, username=username)


@app.route("/view_driver/<driver_id>")
def view_driver(driver_id):
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles=Adolf_Brudes")
    print(response)
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    drivers = mongo.db.drivers.find_one({"_id": ObjectId(driver_id)})
    results = list(mongo.db.results.find({"driverId": drivers["driverId"]}))
    wins = list(mongo.db.results.find({"driverId": drivers["driverId"], "position": 1}))
    second = list(mongo.db.results.find({"driverId": drivers["driverId"], "position": 2}))
    third = list(mongo.db.results.find({"driverId": drivers["driverId"], "position": 3}))
    
    ## https://stackoverflow.com/questions/59801085/finding-the-main-picture-of-the-wikipedia-page-with-python
    def get_wiki_main_image(title):
        url = 'https://en.wikipedia.org/w/api.php'
        data = {
            'action' :'query',
            'format' : 'json',
            'formatversion' : 2,
            'prop' : 'pageimages|pageterms',
            'piprop' : 'original',
            'titles' : title
        }
        response = requests.get(url, data)
        json_data = json.loads(response.text)
        return json_data['query']['pages'][0]['original']['source'] if len(json_data['query']['pages']) >0 else 'Not found'
    try: 
        image = get_wiki_main_image(drivers["forename"] + " " + drivers["surname"])
    except KeyError:
        image = "../static/img/no_image_available.svg"
    return render_template(
        "view/view_driver.html", results=results, drivers=drivers, wins=wins, second=second, third=third, username=username, image=image)


@app.route("/view_race/<race_id>")
def view_race(race_id):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    races = mongo.db.races.find_one({"_id": ObjectId(race_id)})
    statuses = list(mongo.db.status.find())
    drivers = list(mongo.db.drivers.find())
    seasons = list(mongo.db.seasons.find())
    driver_standings = list(mongo.db.driver_standings.find({"raceId": races["raceId"]}).sort("position", 1))
    circuits = list(mongo.db.circuits.find())
    qualifying = list(mongo.db.qualifying.find({"raceId": races["raceId"]}).sort("position", 1))
    constructors = list(mongo.db.constructors.find())
    constructor_standings = list(mongo.db.constructor_standings.find({"raceId": races["raceId"]}).sort("position", 1))
    results = list(mongo.db.results.find().sort("positionOrder", 1))
    return render_template(
        "view/view_race.html", statuses=statuses, races=races, results=results, drivers=drivers, constructors=constructors, qualifying=qualifying, 
        circuits=circuits, driver_standings=driver_standings, constructor_standings=constructor_standings, seasons=seasons, username=username)

@app.route("/view_season/<season_id>")
def view_season(season_id):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    seasons = mongo.db.seasons.find_one({"_id": ObjectId(season_id)})
    races = list(mongo.db.races.find().sort("round", 1))
    constructors = list(mongo.db.constructors.find({"constructorId": seasons["constructorChampionId"]}))
    circuits = list(mongo.db.circuits.find())
    drivers = list(mongo.db.drivers.find({"driverId": seasons["driverChampionId"]}))
    return render_template(
        "view/view_season.html", races=races, seasons=seasons, constructors=constructors, drivers=drivers, circuits=circuits, username=username)


## AUTH ROUTES

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
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

## PROFILE ROUTES

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
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
        return render_template("profile/profile.html", username=username, display_name=display_name)

    return redirect(url_for("login"))

@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    username = mongo.db.users.find_one(
        {"username": session["user"]})
    if request.method == "POST":
        if check_password_hash(
            username["password"], request.form.get("currentPassword")):
            mongo.db.users.update_one(
            {"username": session["user"]},
            {"$set": {"password": generate_password_hash(request.form.get("newPassword"))}}
        )
            flash("Password has been updated successfully.")
            return redirect(url_for("profile", username=session["user"]))

        else:
            flash("Incorrect Password")
            return redirect(url_for("change_password", username=session["user"]))

    return render_template("profile/change_password.html", username=username)

@app.route("/deleteaccount", methods=["GET", "POST"])
def delete_account():

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
            # invalid password match
            flash("Username does not match.")
            return redirect(url_for("delete_account"))

    return render_template("profile/delete_account.html", username=username)

@app.route("/favourites", methods=["GET", "POST"])
def favourites():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    display_name = mongo.db.users.find_one(
        {"username": session["user"]})["display_name"]
    return render_template("profile/favourites.html", username=username,display_name=display_name)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)

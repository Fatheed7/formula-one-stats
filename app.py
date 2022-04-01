import os

from bson.objectid import ObjectId
from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

def get_pagination_data(offset=0, per_page=20, type = "all"):
    if type == "drivers":
        return mongo.db.drivers.find().sort("driverId", 1).skip(offset).limit(per_page)
    elif type == "circuits":
        return mongo.db.circuits.find().sort("circuitId", 1).skip(offset).limit(per_page)
    elif type == "constructors":
        return mongo.db.constructors.find().sort("constructorId", 1).skip(offset).limit(per_page)
    elif type == "races":
        return mongo.db.races.find().sort("raceId", 1).skip(offset).limit(per_page)
    elif type == "seasons":
        return mongo.db.seasons.find().sort("year", 1).skip(offset).limit(per_page)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.errorhandler(404)
def invalid_route(e):
    return render_template("error/404.html")


@app.route("/circuits")
def circuits():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page=20
    offset = ((page - 1) * per_page)
    circuits = list(mongo.db.circuits.find())
    total = len(circuits)
    pagination_circuits = get_pagination_data(offset=offset, per_page=per_page, type="circuits")
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('circuits.html',
                           circuits=pagination_circuits,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@app.route("/constructors")
def constructors():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page=20
    offset = ((page - 1) * per_page)
    constructors = list(mongo.db.constructors.find())
    total = len(constructors)
    pagination_constructors = get_pagination_data(offset=offset, per_page=per_page, type="constructors")
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('constructors.html',
                           constructors=pagination_constructors,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/drivers")
def drivers():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page=20
    offset = ((page - 1) * per_page)
    drivers = list(mongo.db.drivers.find())
    total = len(drivers)
    pagination_drivers = get_pagination_data(offset=offset, per_page=per_page, type="drivers")
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('drivers.html',
                           drivers=pagination_drivers,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route("/edit_driver/<driver_id>", methods=["GET", "POST"])
def edit_driver(driver_id):
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
    return render_template("edit_driver.html", countries=countries, drivers=drivers)

@app.route("/edit_race/<race_id>", methods=["GET", "POST"])
def edit_race(race_id):
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
    print(previous_race)
    return render_template(
        "edit_race.html", statuses=statuses, races=races, results=results, drivers=drivers, constructors=constructors, qualifying=qualifying, 
        circuits=circuits, driver_standings=driver_standings, constructor_standings=constructor_standings, seasons=seasons, previous_race=previous_race)

@app.route("/races")
def races():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page=20
    offset = ((page - 1) * per_page)
    races = list(mongo.db.races.find())
    seasons = list(mongo.db.seasons.find())
    circuits = list(mongo.db.circuits.find())
    total = len(races)
    pagination_races = get_pagination_data(offset=offset, per_page=per_page, type="races")
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('races.html',
                           races=pagination_races,
                           seasons=seasons,
                           circuits=circuits,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@app.route("/seasons")
def seasons():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page=20
    offset = ((page - 1) * per_page)
    seasons = list(mongo.db.seasons.find())
    total = len(seasons)
    pagination_seasons = get_pagination_data(offset=offset, per_page=per_page, type="seasons")
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('seasons.html',
                           seasons=pagination_seasons,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@app.route("/view_circuit/<circuit_id>")
def view_circuit(circuit_id):
    circuits = mongo.db.circuits.find_one({"_id": ObjectId(circuit_id)})
    races = list(mongo.db.races.find().sort("year", 1))
    seasons = list(mongo.db.seasons.find().sort("year", 1))
    print(seasons)
    return render_template(
        "view_circuit.html", races=races, circuits=circuits, seasons=seasons)

@app.route("/view_constructor/<constructor_id>")
def view_constructor(constructor_id):
    constructors = mongo.db.constructors.find_one({"_id": ObjectId(constructor_id)})
    constructor_results = list(mongo.db.constructor_results.find({"constructorId": constructors["constructorId"]}))
    seasons = list(mongo.db.seasons.find({"constructorChampionId": constructors["constructorId"]})) 
    return render_template(
        "view_constructor.html", constructor_results=constructor_results, constructors=constructors, seasons=seasons)


@app.route("/view_driver/<driver_id>")
def view_driver(driver_id):
    drivers = mongo.db.drivers.find_one({"_id": ObjectId(driver_id)})
    results = list(mongo.db.results.find({"driverId": drivers["driverId"]}))
    wins = list(mongo.db.results.find({"driverId": drivers["driverId"], "position": 1}))
    return render_template(
        "view_driver.html", results=results, drivers=drivers, wins=wins)


@app.route("/view_race/<race_id>")
def view_race(race_id):
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
        "view_race.html", statuses=statuses, races=races, results=results, drivers=drivers, constructors=constructors, qualifying=qualifying, 
        circuits=circuits, driver_standings=driver_standings, constructor_standings=constructor_standings, seasons=seasons)

@app.route("/view_season/<season_id>")
def view_season(season_id):
    seasons = mongo.db.seasons.find_one({"_id": ObjectId(season_id)})
    races = list(mongo.db.races.find().sort("round", 1))
    constructors = list(mongo.db.constructors.find({"constructorId": seasons["constructorChampionId"]}))
    print(constructors)
    drivers = list(mongo.db.drivers.find({"driverId": seasons["driverChampionId"]}))
    print(drivers)
    return render_template(
        "view_season.html", races=races, seasons=seasons, constructors=constructors, drivers=drivers)

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
                        flash("Welcome, {}".format(
                            request.form.get("username")))
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

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)

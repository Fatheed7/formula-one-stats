import base64
from io import BytesIO
import os

from bson.objectid import ObjectId
from flask import (Blueprint, Flask, flash, redirect, render_template, request,
                   session, url_for)
from matplotlib.figure import Figure
from flask_paginate import Pagination, get_page_parameter
from flask_pymongo import PyMongo

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
    return render_template("home.html")



@app.route("/circuits")
def circuits():
    circuits = list(mongo.db.circuits.find())
    return render_template("circuits.html", circuits=circuits)


@app.route("/constructors")
def constructors():
    constructors = list(mongo.db.constructors.find())
    return render_template("constructors.html", constructors=constructors)


@app.route("/drivers")
def drivers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    drivers = list(mongo.db.drivers.find())
    per_page = 20
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(drivers))
    return render_template("drivers.html", drivers=drivers, pagination = pagination)

@app.route("/edit_drivers/<driver_id>", methods=["GET", "POST"])
def edit_drivers(driver_id):
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
        mongo.db.drivers.update({"_id": ObjectId(driver_id)}, submit)

    drivers = mongo.db.drivers.find_one({"_id": ObjectId(driver_id)})
    countries = list(mongo.db.countries.find().sort("nationality", 1))
    return render_template("edit_drivers.html", countries=countries, drivers=drivers)

@app.route("/races")
def races():
    races = list(mongo.db.races.find())
    seasons = list(mongo.db.seasons.find())
    circuits = list(mongo.db.circuits.find())
    return render_template("races.html", races=races, seasons=seasons, circuits=circuits)


@app.route("/seasons")
def seasons():
    seasons = list(mongo.db.seasons.find().sort("year", 1))
    return render_template("seasons.html", seasons=seasons)


@app.route("/view_circuit/<circuit_id>")
def view_circuit(circuit_id):
    circuits = mongo.db.circuits.find_one({"_id": ObjectId(circuit_id)})
    races = list(mongo.db.races.find().sort("year", 1))
    return render_template(
        "view_circuit.html", races=races, circuits=circuits)


@app.route("/view_race/<race_id>")
def view_race(race_id):
    races = mongo.db.races.find_one({"_id": ObjectId(race_id)})
    statuses = list(mongo.db.status.find())
    drivers = list(mongo.db.drivers.find())
    seasons = list(mongo.db.seasons.find())
    driver_standings = list(mongo.db.driver_standings.find().sort("position", 1))
    circuits = list(mongo.db.circuits.find())
    qualifying = list(mongo.db.qualifying.find().sort("position", 1))
    constructors = list(mongo.db.constructors.find())
    constructor_standings = list(mongo.db.constructor_standings.find().sort("position", 1))
    results = list(mongo.db.results.find().sort("position", 1))
    return render_template(
        "view_race.html", statuses=statuses, races=races, results=results, drivers=drivers, constructors=constructors, qualifying=qualifying, 
        circuits=circuits, driver_standings=driver_standings, constructor_standings=constructor_standings, seasons=seasons)

@app.route("/view_season/<season_id>")
def view_season(season_id):
    seasons = mongo.db.seasons.find_one({"_id": ObjectId(season_id)})
    races = list(mongo.db.races.find().sort("round", 1))
    return render_template(
        "view_season.html", races=races, seasons=seasons)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)

import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for, Blueprint
    )
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_parameter

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
    page_size = 20
    page = request.args.get(get_page_parameter(), type=int, default=1)
    drivers = list(mongo.db.drivers.find())
    pagination = Pagination(page=page, per_page=page_size,total=len(drivers))
    return render_template("drivers.html", drivers=drivers, pagination=pagination)

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
            "url": request.form.get("url")
        }
        mongo.db.drivers.update({"_id": ObjectId(driver_id)}, submit)
        flash("Category Successfully Updated")

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
    seasons = list(mongo.db.seasons.find())
    return render_template("seasons.html", seasons=seasons)


@app.route("/statuses")
def statuses():
    status = list(mongo.db.status.find().sort("statusId", 1))
    return render_template("statuses.html", status=status)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for
    )
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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
    drivers = list(mongo.db.drivers.find())
    return render_template("drivers.html", drivers=drivers)


@app.route("/seasons")
def seasons():
    seasons = list(mongo.db.seasons.find())
    races = list(mongo.db.races.find())
    return render_template("seasons.html", seasons=seasons, races=races)


@app.route("/statuses")
def statuses():
    status = list(mongo.db.status.find().sort("statusId", 1))
    return render_template("statuses.html", status=status)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
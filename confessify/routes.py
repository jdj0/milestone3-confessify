from flask import render_template
from confessify import app, db
from confessify.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/confess")
def confess():
    return render_template("confess.html")

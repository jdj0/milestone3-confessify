from flask import render_template
from confessify import app, db
from confessify.models import User, Post


@app.route("/")
def home():
    return render_template("base.html")
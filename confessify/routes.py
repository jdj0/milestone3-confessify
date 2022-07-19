from flask import Flask, flash, render_template, request, url_for, redirect
from confessify import app, db
from confessify.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Create exisiting username variable
        existing_user = User.query.filter(User.username == request.form.get("username").lower()).all()
        # Check availability of username
        if existing_user:
            flash("Username already taken")
            return redirect(url_for("register"))

        new_user = User(
            username = request.form.get('username').lower(),
            password = generate_password_hash(request.form.get('password1'))
        )

        # enter new_user to the database
        db.session.add(new_user)
        db.session.commit()
        flash("Sign up Successful")

    return render_template("register.html")


@app.route("/confess")
def confess():
    return render_template("confess.html")
from flask import Flask, flash, render_template, request, url_for, redirect, session
from confessify import app, db
from confessify.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Search database for username
        existing_user = User.query.filter(User.username == request.form.get('username-login').lower()).all()

        if existing_user:
            if check_password_hash(existing_user[0].password, request.form.get('password-login')):
                session["user"] = request.form.get("username-login").lower()
                flash("Welcome")
            else:
                flash("Incorrect login details")
                return redirect(url_for("home"))
        else:
            flash("Incorrect login details")
            return redirect(url_for("home"))

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
        # check passwords match
        if request.form.get('password1') != request.form.get('password2'):
            flash("Passwords do not match")
            return redirect(url_for("register"))
        # create new user entry for database
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
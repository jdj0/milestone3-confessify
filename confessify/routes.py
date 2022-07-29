from flask import Flask, flash, render_template, request, url_for, redirect, session
from confessify import app, db
from confessify.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        existing_user = User.query.filter(User.username == request.form.get('username-login').lower()).all()
        # Search database for username
        if existing_user:
            if check_password_hash(existing_user[0].password, request.form.get('password-login')):
                session["user"] = request.form.get("username-login").lower()
                flash("Welcome")
                return render_template("profile.html")
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


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        
        user = User.query.filter(User.username == session["user"].lower()).first()

        post = Post(
            post_title = request.form.get('post_title'),
            post_content = request.form.get('post_content'),
            user_id = user.id
        )
        
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("profile.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# @app.route("/profile/<username>", methods=["GET", "POST"])
# def profile(username):
#     if "user" in session:
#         username = session["user"]
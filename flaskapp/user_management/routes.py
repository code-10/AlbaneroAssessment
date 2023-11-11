from urllib.parse import urlencode
import secrets
import requests
from . import blueprint
from .models import User
from .service import get_user_by_email
from .forms import RegisterForm, LoginForm
from flaskapp.sqlite_database import db
from flask import request, flash, render_template, redirect, url_for, abort, current_app, session
from flask_login import login_user, logout_user, current_user

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = get_user_by_email(form.email.data)
            if user is None:
                flash("Invalid Username")
            else:
                if user.verify_hash(form.password.data):
                    login_user(user)
                    next = request.args.get("next")
                    return redirect(next or url_for("train.ticket_meta"))
                else:
                    flash("Login Fail")
    return render_template("user/login.html", form=form)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.generate_hash(form.password.data)
            userAlreadyExists = get_user_by_email(form.email.data)
            if not userAlreadyExists.email:
                db.session.add(user)
                db.session.commit()
                current_app.logger.info("User Already Registerd: %s", user.email)
                return redirect(url_for("user_management.register"))
            return redirect(url_for("user_management.login"))
    return render_template("user/register.html", form=form)


@blueprint.get("/logout")
def logout():
    logout_user()
    current_app.logger.info("User Logged Out")
    return redirect(url_for("user_management.login"))



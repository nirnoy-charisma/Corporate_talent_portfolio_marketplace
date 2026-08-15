from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models import db
from models.user import User
from patterns.user_factory import UserFactory

from models.individual_profile import IndividualProfile
from models.company_profile import CompanyProfile
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_type = request.form["user_type"]
        name_value = request.form["fullName"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered.")
            return redirect(url_for("home"))

        extra_fields = {}
        if user_type == "individual":
            extra_fields["fullName"] = name_value
        elif user_type == "company":
            extra_fields["companyName"] = name_value

        user, profile = UserFactory.create_user(email, password, user_type, **extra_fields)

        session["userId"] = user.userId
        session["userType"] = user.userType
        return redirect(url_for("auth.dashboard"))

    return redirect(url_for("home"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwordHash, password):
            session["userId"] = user.userId
            session["userType"] = user.userType
            return redirect(url_for("auth.dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("home"))

    return redirect(url_for("home"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))





@auth_bp.route("/dashboard")
def dashboard():
    if "userId" not in session:
        return redirect(url_for("home"))

    user_type = session["userType"]
    if user_type == "individual":
        profile = IndividualProfile.query.filter_by(userId=session["userId"]).first()
        display_name = profile.fullName if profile else "User"
    elif user_type == "company":
        profile = CompanyProfile.query.filter_by(userId=session["userId"]).first()
        display_name = profile.companyName if profile else "Company"
    else:
        display_name = "User"

    return render_template("dashboard.html", display_name=display_name)
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.individual_profile import IndividualProfile
from patterns.portfolio_builder import BUILDER_MAP, UploadDirector

portfolio_bp = Blueprint("portfolio", __name__)


@portfolio_bp.route("/portfolio/upload", methods=["GET", "POST"])
def upload():
    if "userId" not in session or session.get("userType") != "individual":
        flash("Only individual accounts can upload portfolio items.")
        return redirect(url_for("home"))

    profile = IndividualProfile.query.filter_by(userId=session["userId"]).first()

    if request.method == "POST":
        category = request.form["category"]
        title = request.form["title"]
        file_url = request.form["file_url"]
        visibility = request.form["visibility"]

        builder_class = BUILDER_MAP.get(category)
        if not builder_class:
            flash("Unknown category.")
            return redirect(url_for("portfolio.upload"))

        builder = builder_class(profile.profileId)
        director = UploadDirector(builder)

        try:
            director.standard_upload(title, file_url, visibility)
            flash("Portfolio item uploaded successfully!")
        except ValueError as e:
            flash(str(e))

        return redirect(url_for("portfolio.upload"))

    attachments = profile.attachments
    return render_template("portfolio_upload.html", attachments=attachments)
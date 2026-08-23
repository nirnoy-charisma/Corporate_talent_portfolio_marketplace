import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from models.individual_profile import IndividualProfile
from patterns.portfolio_builder import BUILDER_MAP, UploadDirector
from patterns.attachment_proxy import AttachmentAccessProxy
from patterns.attachment_decorator import BasicAttachmentDisplay, VerifiedBadgeDecorator, FeaturedBadgeDecorator
from patterns.portfolio_composite import build_portfolio_tree

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
        visibility = request.form["visibility"]

        builder_class = BUILDER_MAP.get(category)
        if not builder_class:
            flash("Unknown category.")
            return redirect(url_for("portfolio.upload"))

        try:
            if category == "project":
                file_value = request.form.get("project_link", "").strip()
                if not file_value:
                    raise ValueError("Please enter a project link.")
            else:
                uploaded_file = request.files.get("file")
                if not uploaded_file or uploaded_file.filename == "":
                    raise ValueError("Please choose a file to upload.")

                ext = os.path.splitext(uploaded_file.filename)[1].lower()
                safe_name = f"{uuid.uuid4().hex}{ext}"
                save_path = os.path.join(current_app.root_path, "static", "uploads", safe_name)
                uploaded_file.save(save_path)
                file_value = f"uploads/{safe_name}"

            builder = builder_class(profile.profileId)
            director = UploadDirector(builder)
            director.standard_upload(title, file_value, visibility)

            flash("Portfolio item uploaded successfully!")
        except ValueError as e:
            flash(str(e))

        return redirect(url_for("portfolio.upload"))

    attachments = profile.attachments
    attachment_displays = []
    for a in attachments:
        display = BasicAttachmentDisplay(a)
        if a.visibilityLevel == "verified_companies":
            display = VerifiedBadgeDecorator(display)
        attachment_displays.append({"rendered": display.render(), "raw": a})

    return render_template("portfolio_upload.html", attachments=attachments, attachment_displays=attachment_displays)


@portfolio_bp.route("/portfolio/view/<profile_id>")
def view_candidate_portfolio(profile_id):
    if "userId" not in session:
        return redirect(url_for("home"))

    profile = IndividualProfile.query.get(profile_id)
    if not profile:
        flash("Profile not found.")
        return redirect(url_for("home"))

    proxy = AttachmentAccessProxy(session["userId"], session["userType"])
    visible_attachments = proxy.get_attachments(profile_id)

    return render_template("view_candidate.html", profile=profile, attachments=visible_attachments)


@portfolio_bp.route("/portfolio/overview")
def portfolio_overview():
    if "userId" not in session or session.get("userType") != "individual":
        return redirect(url_for("home"))

    profile = IndividualProfile.query.filter_by(userId=session["userId"]).first()
    tree = build_portfolio_tree(profile.attachments)

    return f"<pre>{tree.render()}</pre>"
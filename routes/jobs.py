from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.company_profile import CompanyProfile
from models.job_vacancy import JobVacancy
from patterns.application_facade import ApplicationFacade
from models.application import Application
from models.company_profile import CompanyProfile
jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/jobs/post", methods=["GET", "POST"])
def post_job():
    if "userId" not in session or session.get("userType") != "company":
        flash("Only company accounts can post jobs.")
        return redirect(url_for("home"))

    company = CompanyProfile.query.filter_by(userId=session["userId"]).first()

    if request.method == "POST":
        job = JobVacancy(
            companyId=company.companyId,
            title=request.form["title"],
            requirements=request.form["requirements"],
            salaryMin=request.form.get("salaryMin") or None,
            salaryMax=request.form.get("salaryMax") or None,
            roleType=request.form["roleType"],
            status="open"
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully!")
        return redirect(url_for("jobs.post_job"))

    my_jobs = JobVacancy.query.filter_by(companyId=company.companyId).order_by(JobVacancy.postedDate.desc()).all()
    return render_template("post_job.html", jobs=my_jobs)


@jobs_bp.route("/jobs/close/<job_id>")
def close_job(job_id):
    if "userId" not in session or session.get("userType") != "company":
        return redirect(url_for("home"))

    job = JobVacancy.query.get(job_id)
    company = CompanyProfile.query.filter_by(userId=session["userId"]).first()

    if job and job.companyId == company.companyId:
        job.status = "closed"
        db.session.commit()
        flash("Job closed.")

    return redirect(url_for("jobs.post_job"))
@jobs_bp.route("/jobs/browse")
def browse_jobs():
    if "userId" not in session or session.get("userType") != "individual":
        flash("Only individual accounts can browse jobs.")
        return redirect(url_for("home"))

    role_filter = request.args.get("roleType")

    query = JobVacancy.query.filter_by(status="open")
    if role_filter:
        query = query.filter_by(roleType=role_filter)

    jobs = query.order_by(JobVacancy.postedDate.desc()).all()
    return render_template("browse_jobs.html", jobs=jobs, active_filter=role_filter)


@jobs_bp.route("/jobs/apply/<job_id>")
def apply_to_job(job_id):
    if "userId" not in session or session.get("userType") != "individual":
        flash("Only individual accounts can apply to jobs.")
        return redirect(url_for("home"))

    try:
        ApplicationFacade().apply_to_job(session["userId"], job_id)
        flash("Application submitted successfully!")
    except ValueError as e:
        flash(str(e))

    return redirect(url_for("jobs.browse_jobs"))


@jobs_bp.route("/jobs/applicants")
def view_applicants():
    if "userId" not in session or session.get("userType") != "company":
        flash("Only company accounts can view applicants.")
        return redirect(url_for("home"))

    company = CompanyProfile.query.filter_by(userId=session["userId"]).first()
    company_jobs = JobVacancy.query.filter_by(companyId=company.companyId).all()
    job_ids = [j.jobId for j in company_jobs]

    applications = Application.query.filter(Application.jobId.in_(job_ids)).order_by(Application.appliedDate.desc()).all()
    return render_template("applicants.html", applications=applications)


@jobs_bp.route("/jobs/applicants/status/<application_id>/<new_status>")
def update_application_status(application_id, new_status):
    if "userId" not in session or session.get("userType") != "company":
        return redirect(url_for("home"))

    application = Application.query.get(application_id)
    if application:
        application.changeStatus(new_status)  # triggers Observer notifications
        flash(f"Application status updated to {new_status}")

    return redirect(url_for("jobs.view_applicants"))
from models import db
from models.application import Application
from models.job_vacancy import JobVacancy
from models.individual_profile import IndividualProfile


class ApplicationFacade:
    """
    Coordinates the multi-step 'apply to job' flow behind one method,
    matching the Application Server (API) lane in the sequence diagram:
    validate -> fetch portfolio snapshot -> insert Application -> confirm.
    """

    def apply_to_job(self, user_id: str, job_id: str) -> Application:
        # Step 1: validate ownership / that the profile exists
        profile = IndividualProfile.query.filter_by(userId=user_id).first()
        if not profile:
            raise ValueError("No individual profile found for this account.")

        # Step 2: validate the job exists and is open
        job = JobVacancy.query.get(job_id)
        if not job or job.status != "open":
            raise ValueError("This job is not currently accepting applications.")

        # Step 3: prevent duplicate applications
        existing = Application.query.filter_by(profileId=profile.profileId, jobId=job_id).first()
        if existing:
            raise ValueError("You've already applied to this job.")

        # Step 4: fetch portfolio snapshot (titles of current attachments)
        attachment_titles = [a.title for a in profile.attachments]
        snapshot = ", ".join(attachment_titles) if attachment_titles else "No portfolio items yet"

        # Step 5: create the Application record
        application = Application(
            jobId=job_id,
            profileId=profile.profileId,
            portfolioSnapshot=snapshot,
            status="Applied"
        )
        db.session.add(application)
        db.session.commit()

        # Step 6: (Observer will plug in right here later, notifying the company)

        return application
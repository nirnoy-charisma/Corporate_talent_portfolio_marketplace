import uuid
from datetime import datetime
from models import db

class Application(db.Model):
    __tablename__ = "application"

    applicationId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    jobId = db.Column(db.String(36), db.ForeignKey("job_vacancy.jobId"), nullable=False)
    profileId = db.Column(db.String(36), db.ForeignKey("individual_profile.profileId"), nullable=False)
    portfolioSnapshot = db.Column(db.Text)
    status = db.Column(db.String(30), default="Applied")
    appliedDate = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship("JobVacancy", backref="applications")
    profile = db.relationship("IndividualProfile", backref="applications")

    def changeStatus(self, newStatus: str):
        """Matches Application.changeStatus(newStatus) from your class diagram.
        Updates status AND notifies observers — this is the Subject/Observer trigger point."""
        from patterns.observer import get_application_subject

        self.status = newStatus
        db.session.commit()

        subject = get_application_subject()
        subject.notify_observers(
            event="application_status_changed",
            payload={
                "applicationId": self.applicationId,
                "jobTitle": self.job.title,
                "status": newStatus,
                "candidateProfileId": self.profileId,
            }
        )

    def __repr__(self):
        return f"<Application {self.profileId} -> {self.jobId} ({self.status})>"
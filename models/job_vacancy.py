import uuid
from datetime import datetime
from models import db

class JobVacancy(db.Model):
    __tablename__ = "job_vacancy"

    jobId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    companyId = db.Column(db.String(36), db.ForeignKey("company_profile.companyId"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    requirements = db.Column(db.Text)
    salaryMin = db.Column(db.Numeric(12, 2))
    salaryMax = db.Column(db.Numeric(12, 2))
    roleType = db.Column(db.String(50))  # e.g. 'remote', 'on-site', 'hybrid'
    status = db.Column(db.String(20), default="open")  # 'open', 'closed'
    postedDate = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("CompanyProfile", backref="job_vacancies")

    def __repr__(self):
        return f"<JobVacancy {self.title}>"
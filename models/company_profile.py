import uuid
from models import db

class CompanyProfile(db.Model):
    __tablename__ = "company_profile"

    companyId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = db.Column(db.String(36), db.ForeignKey("user.userId"), nullable=False, unique=True)
    companyName = db.Column(db.String(255), nullable=False)
    regDoc = db.Column(db.String(500))  # file path/URL to registration document
    verificationStatus = db.Column(db.String(30), default="pending")  # 'pending', 'verified', 'rejected'
    industry = db.Column(db.String(100))

    user = db.relationship("User", backref="company_profile")

    def __repr__(self):
        return f"<CompanyProfile {self.companyName} ({self.verificationStatus})>"
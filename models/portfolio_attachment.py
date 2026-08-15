import uuid
from datetime import datetime
from models import db

class PortfolioAttachment(db.Model):
    __tablename__ = "portfolio_attachment"

    attachmentId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profileId = db.Column(db.String(36), db.ForeignKey("individual_profile.profileId"), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'certificate', 'project', 'other'
    title = db.Column(db.String(255), nullable=False)
    fileUrl = db.Column(db.String(500), nullable=False)  # PDF path, image path, or a link
    visibilityLevel = db.Column(db.String(30), default="public")  # 'public', 'private', 'verified_companies'
    datePublished = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("IndividualProfile", backref="attachments")

    def __repr__(self):
        return f"<PortfolioAttachment {self.title}>"
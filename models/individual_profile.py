import uuid
from models import db

class IndividualProfile(db.Model):
    __tablename__ = "individual_profile"

    profileId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = db.Column(db.String(36), db.ForeignKey("user.userId"), nullable=False, unique=True)
    fullName = db.Column(db.String(255), nullable=False)
    headline = db.Column(db.String(255))
    experienceLevel = db.Column(db.String(50))  # e.g. 'entry', 'mid', 'senior'
    profileVisibility = db.Column(db.String(30), default="public")  # 'public', 'private', 'verified_companies'

    user = db.relationship("User", backref="individual_profile")

    def __repr__(self):
        return f"<IndividualProfile {self.fullName}>"
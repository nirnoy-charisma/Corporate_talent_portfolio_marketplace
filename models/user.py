import uuid
from datetime import datetime
from models import db

class User(db.Model):
    __tablename__ = "user"

    userId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    userType = db.Column(db.String(20), nullable=False)  # 'individual', 'company', 'admin'
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email} ({self.userType})>"
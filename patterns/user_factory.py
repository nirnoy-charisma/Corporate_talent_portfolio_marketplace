import uuid
from models import db
from models.user import User
from models.individual_profile import IndividualProfile
from models.company_profile import CompanyProfile
from werkzeug.security import generate_password_hash


class UserFactory:
    @staticmethod
    def create_user(email: str, password: str, user_type: str, **extra_fields):
        """
        Creates a User row AND the correct linked profile row
        (IndividualProfile or CompanyProfile) in one call.
        This is the Factory Method: the caller (the route) doesn't
        need to know which profile class to instantiate.
        """
        new_user = User(
            userId=str(uuid.uuid4()),
            email=email,
            passwordHash=generate_password_hash(password),
            userType=user_type
        )
        db.session.add(new_user)
        db.session.flush()  # gets new_user.userId available without full commit yet

        if user_type == "individual":
            profile = IndividualProfile(
                profileId=str(uuid.uuid4()),
                userId=new_user.userId,
                fullName=extra_fields.get("fullName"),
                headline=extra_fields.get("headline", ""),
                experienceLevel=extra_fields.get("experienceLevel", "entry"),
                profileVisibility="public"
            )
        elif user_type == "company":
            profile = CompanyProfile(
                companyId=str(uuid.uuid4()),
                userId=new_user.userId,
                companyName=extra_fields.get("companyName"),
                industry=extra_fields.get("industry", ""),
                verificationStatus="pending"
            )
        else:
            raise ValueError(f"Unknown user_type: {user_type}")

        db.session.add(profile)
        db.session.commit()
        return new_user, profile
import uuid
from abc import ABC, abstractmethod
from models import db
from models.user import User
from models.individual_profile import IndividualProfile
from models.company_profile import CompanyProfile
from werkzeug.security import generate_password_hash


class UserCreator(ABC):
    """Abstract Creator — declares the factory method, matches ShipCreator."""

    @abstractmethod
    def factory_method(self, email, password, user, **extra_fields):
        """Subclasses override this to build the correct profile type."""
        pass

    def create_user_and_profile(self, email, password, user_type, **extra_fields):
        """Template method — identical for every subclass, matches CreateShip()."""
        new_user = User(
            userId=str(uuid.uuid4()),
            email=email,
            passwordHash=generate_password_hash(password),
            userType=user_type
        )
        db.session.add(new_user)
        db.session.flush()  # assigns new_user.userId without full commit yet

        profile = self.factory_method(email, password, new_user, **extra_fields)

        db.session.add(profile)
        db.session.commit()
        return new_user, profile


class IndividualUserCreator(UserCreator):
    """Concrete Creator — matches DestroyerCreator."""

    def factory_method(self, email, password, user, **extra_fields):
        return IndividualProfile(
            profileId=str(uuid.uuid4()),
            userId=user.userId,
            fullName=extra_fields.get("fullName"),
            headline=extra_fields.get("headline", ""),
            experienceLevel=extra_fields.get("experienceLevel", "entry"),
            profileVisibility="public"
        )


class CompanyUserCreator(UserCreator):
    """Concrete Creator — matches CarrierCreator."""

    def factory_method(self, email, password, user, **extra_fields):
        return CompanyProfile(
            companyId=str(uuid.uuid4()),
            userId=user.userId,
            companyName=extra_fields.get("companyName"),
            industry=extra_fields.get("industry", ""),
            verificationStatus="pending"
        )

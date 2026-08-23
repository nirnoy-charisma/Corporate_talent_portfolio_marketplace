from models.individual_profile import IndividualProfile
from models.company_profile import CompanyProfile


class AuthService:
    """
    Singleton — matches lecture's private constructor + static getInstance().
    Takes NO parameters, per lecture's explicit rule.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        """Matches lecture's getInstance() naming convention exactly."""
        if AuthService._instance is None:
            AuthService._instance = AuthService()
        return AuthService._instance

    def can_view_attachment(self, viewer_user_id: str, viewer_user_type: str, attachment) -> bool:
        """
        Central visibility rule, used by the Proxy (pattern #2 below).
        One shared service, used everywhere access decisions are made.
        """
        level = attachment.visibilityLevel

        if level == "public":
            return True

        if level == "private":
            owner_profile = IndividualProfile.query.get(attachment.profileId)
            return owner_profile is not None and owner_profile.userId == viewer_user_id

        if level == "verified_companies":
            if viewer_user_type != "company":
                return False
            company = CompanyProfile.query.filter_by(userId=viewer_user_id).first()
            return company is not None and company.verificationStatus == "verified"

        return False
from abc import ABC, abstractmethod
from models.portfolio_attachment import PortfolioAttachment
from patterns.auth_singleton import AuthService


# ---- Subject interface ----
class AttachmentAccessSubject(ABC):
    @abstractmethod
    def get_attachments(self, profile_id: str):
        pass


# ---- RealSubject — does the actual work, no access control ----
class RealAttachmentAccess(AttachmentAccessSubject):
    def get_attachments(self, profile_id: str):
        return PortfolioAttachment.query.filter_by(profileId=profile_id).all()


# ---- Proxy — same interface, adds access control before delegating ----
class AttachmentAccessProxy(AttachmentAccessSubject):
    def __init__(self, viewer_user_id: str, viewer_user_type: str):
        self._real_subject = RealAttachmentAccess()
        self.viewer_user_id = viewer_user_id
        self.viewer_user_type = viewer_user_type

    def get_attachments(self, profile_id: str):
        """
        Fetches from RealSubject, then filters using the Singleton AuthService
        BEFORE returning anything to the caller — this is the access-control
        gate matching your lecture's whitelist/blacklist Proxy example.
        """
        all_attachments = self._real_subject.get_attachments(profile_id)
        auth = AuthService.get_instance()

        visible = [
            a for a in all_attachments
            if auth.can_view_attachment(self.viewer_user_id, self.viewer_user_type, a)
        ]
        return visible
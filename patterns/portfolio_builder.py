import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from models import db
from models.portfolio_attachment import PortfolioAttachment
from patterns.attachment_factory import get_attachment_factory


# ---- Abstract Builder (matches SandwichBuilder) ----
class PortfolioAttachmentBuilder(ABC):
    """
    Declares the build steps. Every concrete builder implements
    these the same way SandwichBuilder declares AddBread/AddProtein/etc.
    """

    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.product = {
            "attachmentId": str(uuid.uuid4()),
            "profileId": profile_id,
            "category": None,
            "title": None,
            "fileUrl": None,
            "visibilityLevel": "public",
            "datePublished": datetime.utcnow(),
        }

    @abstractmethod
    def add_category(self):
        pass

    @abstractmethod
    def add_title(self, title: str):
        pass

    @abstractmethod
    def add_file_url(self, file_url: str):
        """Each concrete builder validates using its matching Abstract Factory validator."""
        pass

    def set_visibility(self, level: str):
        """Shared step — same for every category, so it lives in the abstract class."""
        self.product["visibilityLevel"] = level

    def return_product(self) -> PortfolioAttachment:
        attachment = PortfolioAttachment(**self.product)
        db.session.add(attachment)
        db.session.commit()
        return attachment


# ---- Concrete Builders (match BurgerBuilder / HotdogBuilder / BLTBuilder) ----
class CertificateBuilder(PortfolioAttachmentBuilder):
    def add_category(self):
        self.product["category"] = "certificate"

    def add_title(self, title: str):
        self.product["title"] = title

    def add_file_url(self, file_url: str):
        validator = get_attachment_factory("certificate").create_validator()
        if not validator.validate(file_url):
            raise ValueError("Certificate must be a .pdf file")
        self.product["fileUrl"] = file_url


class ProjectBuilder(PortfolioAttachmentBuilder):
    def add_category(self):
        self.product["category"] = "project"

    def add_title(self, title: str):
        self.product["title"] = title

    def add_file_url(self, file_url: str):
        validator = get_attachment_factory("project").create_validator()
        if not validator.validate(file_url):
            raise ValueError("Project must be a link (http/https)")
        self.product["fileUrl"] = file_url


class PhotoBuilder(PortfolioAttachmentBuilder):
    def add_category(self):
        self.product["category"] = "photo"

    def add_title(self, title: str):
        self.product["title"] = title

    def add_file_url(self, file_url: str):
        validator = get_attachment_factory("photo").create_validator()
        if not validator.validate(file_url):
            raise ValueError("Photo must be .jpg, .jpeg, or .png")
        self.product["fileUrl"] = file_url


BUILDER_MAP = {
    "certificate": CertificateBuilder,
    "project": ProjectBuilder,
    "photo": PhotoBuilder,
}


# ---- Director (matches your lecture's Director class exactly) ----
class UploadDirector:
    """
    Defines the ORDER in which build steps run.
    The builder defines HOW each step works — same separation as
    DineInOrder()/TakeoutOrder()/NoSauce()/NoSides() in your slides.
    """

    def __init__(self, builder: PortfolioAttachmentBuilder):
        self.builder = builder

    def standard_upload(self, title: str, file_url: str, visibility: str) -> PortfolioAttachment:
        """Normal upload: category -> title -> file -> visibility."""
        self.builder.add_category()
        self.builder.add_title(title)
        self.builder.add_file_url(file_url)   # this is where validation happens
        self.builder.set_visibility(visibility)
        return self.builder.return_product()

    def quick_public_upload(self, title: str, file_url: str) -> PortfolioAttachment:
        """Quick upload: skips visibility step entirely, defaults stay 'public'."""
        self.builder.add_category()
        self.builder.add_title(title)
        self.builder.add_file_url(file_url)
        return self.builder.return_product()

    def verified_only_upload(self, title: str, file_url: str) -> PortfolioAttachment:
        """Restricted upload: always forces visibility to verified_companies."""
        self.builder.add_category()
        self.builder.add_title(title)
        self.builder.add_file_url(file_url)
        self.builder.set_visibility("verified_companies")
        return self.builder.return_product()
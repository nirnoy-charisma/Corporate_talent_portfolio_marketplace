from abc import ABC, abstractmethod


class AttachmentValidator(ABC):
    @abstractmethod
    def validate(self, file_url: str) -> bool:
        pass


class PdfValidator(AttachmentValidator):
    def validate(self, file_url: str) -> bool:
        return file_url.lower().endswith(".pdf")


class ImageValidator(AttachmentValidator):
    def validate(self, file_url: str) -> bool:
        return file_url.lower().endswith((".jpg", ".jpeg", ".png"))


class LinkValidator(AttachmentValidator):
    def validate(self, file_url: str) -> bool:
        return file_url.lower().startswith(("http://", "https://"))


class AttachmentRenderer(ABC):
    @abstractmethod
    def render(self, title: str) -> str:
        pass


class PdfRenderer(AttachmentRenderer):
    def render(self, title: str) -> str:
        return f"📄 {title}"


class ImageRenderer(AttachmentRenderer):
    def render(self, title: str) -> str:
        return f"🖼️ {title}"


class LinkRenderer(AttachmentRenderer):
    def render(self, title: str) -> str:
        return f"🔗 {title}"


class AttachmentFactory(ABC):
    @abstractmethod
    def create_validator(self) -> AttachmentValidator:
        pass

    @abstractmethod
    def create_renderer(self) -> AttachmentRenderer:
        pass


class PdfAttachmentFactory(AttachmentFactory):
    def create_validator(self): return PdfValidator()
    def create_renderer(self): return PdfRenderer()


class ImageAttachmentFactory(AttachmentFactory):
    def create_validator(self): return ImageValidator()
    def create_renderer(self): return ImageRenderer()


class LinkAttachmentFactory(AttachmentFactory):
    def create_validator(self): return LinkValidator()
    def create_renderer(self): return LinkRenderer()


def get_attachment_factory(category: str) -> AttachmentFactory:
    mapping = {
        "certificate": PdfAttachmentFactory(),
        "project": LinkAttachmentFactory(),
        "photo": ImageAttachmentFactory(),
    }
    factory = mapping.get(category)
    if not factory:
        raise ValueError(f"No factory registered for category: {category}")
    return factory
from abc import ABC, abstractmethod


# ---- Component interface ----
class AttachmentDisplay(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


# ---- ConcreteComponent — matches lecture's base Sandwich/Component ----
class BasicAttachmentDisplay(AttachmentDisplay):
    def __init__(self, attachment):
        self.attachment = attachment

    def render(self) -> str:
        icons = {"certificate": "📄", "photo": "🖼️", "project": "🔗"}
        icon = icons.get(self.attachment.category, "📎")
        return f"{icon} {self.attachment.title}"


# ---- Decorator (abstract) — holds a reference to the wrapped Component ----
class AttachmentDecorator(AttachmentDisplay):
    def __init__(self, wrapped: AttachmentDisplay):
        self._wrapped = wrapped

    def render(self) -> str:
        return self._wrapped.render()


# ---- ConcreteDecorators ----
class VerifiedBadgeDecorator(AttachmentDecorator):
    def render(self) -> str:
        return self._wrapped.render() + " ✅ Verified"


class FeaturedBadgeDecorator(AttachmentDecorator):
    def render(self) -> str:
        return self._wrapped.render() + " ⭐ Featured"
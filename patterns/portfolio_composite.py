from abc import ABC, abstractmethod


# ---- Component ----
class PortfolioComponent(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


# ---- Leaf ----
class AttachmentLeaf(PortfolioComponent):
    def __init__(self, attachment):
        self.attachment = attachment

    def render(self) -> str:
        return f"  - {self.attachment.title}"


# ---- Composite ----
class CategoryGroup(PortfolioComponent):
    def __init__(self, category_name: str):
        self.category_name = category_name
        self._children: list[PortfolioComponent] = []

    def add(self, component: PortfolioComponent):
        self._children.append(component)

    def remove(self, component: PortfolioComponent):
        self._children.remove(component)

    def render(self) -> str:
        lines = [f"{self.category_name}:"]
        for child in self._children:
            lines.append(child.render())
        return "\n".join(lines)


def build_portfolio_tree(attachments) -> CategoryGroup:
    """Groups a flat list of attachments into a Composite tree by category."""
    root = CategoryGroup("Portfolio")
    groups: dict[str, CategoryGroup] = {}

    for attachment in attachments:
        category = attachment.category
        if category not in groups:
            groups[category] = CategoryGroup(category.capitalize())
            root.add(groups[category])
        groups[category].add(AttachmentLeaf(attachment))

    return root
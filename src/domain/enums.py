from enum import Enum

class BudgetStatus(Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    CLOSED = "closed"
    ARCHIVED = "archived"
    LOCKED = "locked"
    REJECTED = "rejected"
    ADJUSTED = "adjusted"

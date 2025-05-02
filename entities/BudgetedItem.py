from typing import List, Dict, Optional
import uuid

class BudgetedItem:
    """
    Represents an individual item in a budget.
    """
    def __init__(self, name: str, description: str, amount: float, category: str, tags: Optional[List[str]] = None):
        self.item_id = str(uuid.uuid4())  # Unique identifier for the item
        self.name = name
        self.description = description
        self.amount = amount
        self.category = category  # e.g., "Needs", "Wants", "Savings"
        self.tags = tags if tags else []

        # Validate item attributes during creation
        self.validate_item()

    def validate_item(self):
        """
        Ensures the item has valid attributes.
        """
        if not self.name or not self.description or self.amount <= 0 or not self.category:
            raise ValueError("Invalid BudgetedItem: All fields must be valid and amount must be > 0.")

    def update_item(self, name: Optional[str] = None, description: Optional[str] = None, 
                    amount: Optional[float] = None, category: Optional[str] = None, 
                    tags: Optional[List[str]] = None):
        """
        Updates the item's attributes.
        """
        if name:
            self.name = name
        if description:
            self.description = description
        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            self.amount = amount
        if category:
            self.category = category
        if tags:
            self.tags = tags

        # Validate updated attributes
        self.validate_item()

    def __repr__(self):
        return (f"BudgetedItem(item_id='{self.item_id}', name='{self.name}', description='{self.description}', "
                f"amount={self.amount}, category='{self.category}', tags={self.tags})")

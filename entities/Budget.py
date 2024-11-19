from typing import List, Dict
from datetime import date
import uuid

class Budget:
    """
    Represents a financial budget over a specified time frame with allocation rules.
    """
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_ARCHIVED = "archived"

    def __init__(self, name: str, start_date: date, end_date: date, 
                 budget_allocated_amount: float, allocation_rule: Dict[str, float]):
        self.budget_id = str(uuid.uuid4())  # Unique identifier for the budget
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.budget_allocated_amount = budget_allocated_amount
        self.allocation_rule = allocation_rule  # e.g., {"Needs": 50, "Wants": 20, "Savings": 30}
        self.status = self.STATUS_OPEN
        self.budgeted_items: List[BudgetedItem] = []

        # Calculate initial unbudgeted amount
        self.unbudgeted_amount = budget_allocated_amount

        # Validate the date range
        self.validate_dates()

    def validate_dates(self):
        """
        Ensures the budget's start and end dates are valid.
        """
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be earlier than end_date.")

    def check_status(self) -> str:
        """
        Returns the current status of the budget.
        """
        return self.status

    def calculate_total_budgeted_amount(self) -> float:
        """
        Calculates the total amount allocated to budgeted items.
        """
        return sum(item.amount for item in self.budgeted_items)

    def calculate_unbudgeted_amount(self) -> float:
        """
        Calculates the unbudgeted amount remaining.
        """
        self.unbudgeted_amount = self.budget_allocated_amount - self.calculate_total_budgeted_amount()
        return self.unbudgeted_amount

    def duplicate_budget(self) -> 'Budget':
        """
        Creates a duplicate of the current budget with a new ID and open status.
        """
        duplicated_budget = Budget(
            name=f"{self.name} (Copy)",
            start_date=self.start_date,
            end_date=self.end_date,
            budget_allocated_amount=self.budget_allocated_amount,
            allocation_rule=self.allocation_rule
        )
        duplicated_budget.budgeted_items = [item for item in self.budgeted_items]
        return duplicated_budget

    def reallocate_budget(self, from_item_id: str, to_item_id: str, amount: float):
        """
        Reallocates a portion of the budgeted amount from one item to another.
        """
        from_item = next((item for item in self.budgeted_items if item.item_id == from_item_id), None)
        to_item = next((item for item in self.budgeted_items if item.item_id == to_item_id), None)

        if not from_item or not to_item:
            raise ValueError("Invalid item IDs for reallocation.")
        if from_item.amount < amount:
            raise ValueError("Insufficient amount in the source item to reallocate.")
        
        # Reallocate the budget
        from_item.amount -= amount
        to_item.amount += amount

    def add_budgeted_item(self, item: BudgetedItem):
        """
        Adds a new budgeted item to the budget.
        """
        if self.status != self.STATUS_OPEN:
            raise ValueError("Cannot add items to a closed or archived budget.")
        if self.unbudgeted_amount < item.amount:
            raise ValueError("Not enough unbudgeted amount available to allocate.")
        self.budgeted_items.append(item)
        self.calculate_unbudgeted_amount()

    def delete_budgeted_item(self, item_id: str):
        """
        Deletes a budgeted item by ID.
        """
        self.budgeted_items = [item for item in self.budgeted_items if item.item_id != item_id]
        self.calculate_unbudgeted_amount()

    def __repr__(self):
        return (f"Budget(budget_id='{self.budget_id}', name='{self.name}', start_date={self.start_date}, "
                f"end_date={self.end_date}, budget_allocated_amount={self.budget_allocated_amount}, "
                f"unbudgeted_amount={self.unbudgeted_amount}, status='{self.status}', "
                f"items={len(self.budgeted_items)})")

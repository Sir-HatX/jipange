from datetime import date, datetime
from ..enums import BudgetStatus
from copy import deepcopy

class Budget:
    __slots__ = ("_budget_id", "_name", "_start_date", "_end_date", "_budget_allocated_amount", "_allocation_rule", "_status")

    def sanitize_name(self, name: str) -> str:
        """Sanitizes the budget name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Budget name must be a non-empty string.")
        return name.strip()

    def __init__(self, budget_id: str, name: str, start_date: date, end_date: date, budget_allocated_amount: float, allocation_rule: dict, status: BudgetStatus = BudgetStatus.DRAFT) -> None:
        self._budget_id = budget_id
        self._name = self.sanitize_name(name)
        self._start_date = start_date
        self._end_date = end_date
        self._budget_allocated_amount = budget_allocated_amount
        self._allocation_rule = allocation_rule
        self._status = status
        self.validate()

    def __setattr__(self, key, value):
        """Restricts direct setting of attributes outside defined methods."""
        if key in self.__slots__:
            # Allow setting attributes directly during initialization
            if not hasattr(self, key):  # Attribute does not exist, allow setting it
                object.__setattr__(self, key, value)
            elif key == "_status" and isinstance(value, BudgetStatus):
                # Allow status to be set via update_status
                object.__setattr__(self, key, value)
            else:
                raise AttributeError(f"Direct modification of '{key}' is not allowed. Use provided methods.")
        else:
            super().__setattr__(key, value)  # For attributes not in __slots__

    # Read-only properties
    @property
    def budget_id(self):
        return self._budget_id

    @budget_id.setter
    def budget_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Budget ID must be a valid non-empty string.")
        self._budget_id = value

    @property
    def name(self):
        return self._name

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def budget_allocated_amount(self):
        return self._budget_allocated_amount

    @property
    def allocation_rule(self):
        return self._allocation_rule

    @property
    def status(self):
        return self._status


    def validate(self):
        if not isinstance(self._budget_id, str) or not self._budget_id.strip():
            raise ValueError("Budget ID must be a valid non-empty string.")

        if not isinstance(self._start_date, date) or not isinstance(self._end_date, date):
            raise ValueError("Start and end dates must be valid date objects.")

        if self._start_date >= self._end_date:
            raise ValueError("End date must be greater than start date.")

        if not isinstance(self._budget_allocated_amount, (int, float)) or self._budget_allocated_amount < 0:
            raise ValueError("Allocated amount must be a positive number.")

        if not isinstance(self._allocation_rule, dict):
            raise ValueError("Allocation rule must be a dictionary.")
        
        if sum(self._allocation_rule.values()) != 100:
            raise ValueError("Allocation rule percentages must sum to 100%.")
        
        if not isinstance(self._status, BudgetStatus):
            raise ValueError("Status must be an instance of BudgetStatus Enum.")
        
    # Methods to control updates
    
    def update_status(self, new_status: BudgetStatus) -> None:
        if not isinstance(new_status, BudgetStatus):
            raise ValueError("Status must be an instance of BudgetStatus Enum.")
        # Allow changing status through the method, but ensure transitions are valid
        # Draft can move to pending approval only
        # Pending approval can move to approved or rejected
        # Approved can move to closed, adjusted, locked
        # Adjusted can move to pending approval
        # Closed can move to archived
        # Locked can only be approved
        valid_transitions = {
            BudgetStatus.DRAFT: {BudgetStatus.PENDING_APPROVAL},
            BudgetStatus.PENDING_APPROVAL: {BudgetStatus.APPROVED, BudgetStatus.REJECTED},
            BudgetStatus.APPROVED: {BudgetStatus.CLOSED, BudgetStatus.ADJUSTED, BudgetStatus.LOCKED},
            BudgetStatus.ADJUSTED: {BudgetStatus.PENDING_APPROVAL},
            BudgetStatus.CLOSED: {BudgetStatus.ARCHIVED},
            BudgetStatus.LOCKED: {BudgetStatus.APPROVED},
        }

        # Special case: allow closing if end_date has passed
        if new_status == BudgetStatus.CLOSED and datetime.now().date() > self.end_date:
            self._status = BudgetStatus.CLOSED
            return

        allowed = valid_transitions.get(self._status, set())
        if new_status in allowed:
            self._status = new_status
        else:
            raise ValueError(f"Invalid status transition from '{self._status.value}' to '{new_status.value}'.")

    def calculate_total_budgeted_amount(self, budgeted_items):
        """Calculates the total amount budgeted for items."""
        if not isinstance(budgeted_items, dict):
            raise ValueError("Budgeted items must be a dictionary of {item: amount}.")
        return sum(budgeted_items.values())

    def calculate_unbudgeted_amount(self, budgeted_items):
        """Calculates the remaining amount that is not budgeted."""
        total_budgeted = self.calculate_total_budgeted_amount(budgeted_items)
        return max(0, self.budget_allocated_amount - total_budgeted)

    def duplicate_budget(self, new_budget_id, new_name=None):
        """Creates a duplicate of the budget with a new ID and optional name."""
        duplicated_budget = deepcopy(self)
        duplicated_budget.budget_id = new_budget_id
        duplicated_budget.name = new_name or f"Copy of {self.name}"
        return duplicated_budget

    def reallocate_budget(self, budgeted_items, source_item, target_item, amount):
        """Reallocates a specified amount from one budget item to another."""
        if source_item not in budgeted_items or target_item not in budgeted_items:
            raise ValueError("Both source and target items must exist in the budgeted items.")
        if amount > budgeted_items[source_item]:
            raise ValueError("Cannot reallocate more than the available amount in the source item.")
        budgeted_items[source_item] -= amount
        budgeted_items[target_item] += amount
        return budgeted_items

    def __repr__(self):
        return (f"Budget(budget_id='{self.budget_id}', name='{self.name}', "
                f"start_date={self.start_date}, end_date={self.end_date}, "
                f"allocated_amount={self.budget_allocated_amount}, "
                f"allocation_rule={self.allocation_rule}, status='{self.status.value}')")

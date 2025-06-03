from datetime import date, datetime

class Budget:
    __slots__ = ("_budget_id", "_name", "_start_date", "_end_date", "_budget_allocated_amount", "_allocation_rule", "_status")

    def sanitize_name(self, name):
        """Sanitizes the budget name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Budget name must be a non-empty string.")
        return name.strip()

    def __init__(self, budget_id, name, start_date, end_date, budget_allocated_amount, allocation_rule, status="draft"):
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
            elif key == "_status" and value in {"draft", "approved", "closed"}:
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

        if self._status not in {"draft", "approved", "closed"}:
            raise ValueError("Status must be 'draft', 'approved', or 'closed'.")
        
    # Methods to control updates
    def update_status(self, new_status):
        valid_statuses = {"draft", "approved", "closed"}
        if new_status not in valid_statuses:
            raise ValueError("Status must be 'draft', 'approved', or 'closed'.")
        
        # Allow changing status through the method, but ensure transitions are valid
        if new_status == "closed" and datetime.now().date() > self.end_date:
            self._status = "closed"
        elif self._status == "draft" and new_status == "approved":
            self._status = "approved"
        elif self._status in {"draft", "approved"} and new_status == "draft":
            self._status = "draft"
        else:
            raise ValueError(f"Invalid status transition from '{self._status}' to '{new_status}'.")

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
                f"allocation_rule={self.allocation_rule}, status='{self.status}')")

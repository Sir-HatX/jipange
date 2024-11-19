from datetime import date
from entity.Budget import Budget  # Import the Budget class
from entity.BudgetedItem import BudgetedItem  # Import the BudgetedItem class

# Define allocation rule: Needs 50%, Wants 20%, Savings 30%
allocation_rule = {"Needs": 50, "Wants": 20, "Savings": 30}

# Create a new budget
oct_budget = Budget(
    name="October 2024 Budget",
    start_date=date(2024, 10, 1),
    end_date=date(2024, 10, 31),
    budget_allocated_amount=2000,
    allocation_rule=allocation_rule
)

# Add budgeted items
item1 = BudgetedItem(name="Rent", description="Monthly rent payment", amount=1000, category="Needs")
item2 = BudgetedItem(name="Groceries", description="Food and essentials", amount=300, category="Needs")
item3 = BudgetedItem(name="Entertainment", description="Movies and games", amount=200, category="Wants")

oct_budget.add_budgeted_item(item1)
oct_budget.add_budgeted_item(item2)
oct_budget.add_budgeted_item(item3)

# Print budget details
print(oct_budget)

# Calculate totals
print("Total Budgeted Amount:", oct_budget.calculate_total_budgeted_amount())
print("Unbudgeted Amount:", oct_budget.calculate_unbudgeted_amount())

# Duplicate the budget
duplicate_budget = oct_budget.duplicate_budget()
print("Duplicated Budget:", duplicate_budget)

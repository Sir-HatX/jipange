from domain.entities.Budget import Budget
from datetime import date

from domain.enums import BudgetStatus

# Create a Budget instance
budget = Budget(
    budget_id="BUDGET123",
    name="Aug 2025 Budget",
    start_date=date(2025, 8, 1),
    end_date=date(2025, 8, 31),
    budget_allocated_amount=1000.0,
    allocation_rule={"Needs": 50, "Wants": 30, "Savings": 20},
    status= BudgetStatus.DRAFT
)

# Print the budget object
print(budget)
# print("===========================")
# Update the status and print
budget.update_status(BudgetStatus.APPROVED)
print("Updated Status:", budget.status)
print("===========================")
# Update the status of the budget
budget.update_status(BudgetStatus.CLOSED)
print("Updated Status:", budget.status)

# Example budgeted items
budgeted_items = {"Rent": 400, "Groceries": 700, "Entertainment": 150}
print("============================")
print("Total Budgeted Amount:", budget.calculate_total_budgeted_amount(budgeted_items))
print("============================")
print("Unbudgeted Amount:", budget.calculate_unbudgeted_amount(budgeted_items))

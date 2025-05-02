from entities.Budget import Budget
from datetime import date

# Create a Budget instance
budget = Budget(
    budget_id="BUDGET123",
    name="October 2024 Budget",
    start_date=date(2024, 10, 1),
    end_date=date(2024, 10, 20),
    budget_allocated_amount=1000.0,
    allocation_rule={"Needs": 50, "Wants": 30, "Savings": 20},
    status="draft"
)

# budget.budget_id = "nwiegnm49ngmin395"

# Print the budget object
print(budget)

# Update the status and print
# budget.update_status("approved")
print("Updated Status:", budget.status)

# Update the status of the budget
# budget.update_status("canceled")
# print("Updated Status:", budget.status)

# Example budgeted items
budgeted_items = {"Rent": 400, "Groceries": 700, "Entertainment": 150}
print("Total Budgeted Amount:", budget.calculate_total_budgeted_amount(budgeted_items))
print("Unbudgeted Amount:", budget.calculate_unbudgeted_amount(budgeted_items))

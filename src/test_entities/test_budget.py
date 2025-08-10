import pytest
from datetime import date, timedelta
from copy import deepcopy
from entities.budget.Budget import Budget


@pytest.fixture
def valid_budget_data():
    return {
        "budget_id": "B001",
        "name": "Marketing Budget",
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=30),
        "budget_allocated_amount": 10000,
        "allocation_rule": {"ads": 50, "events": 30, "software": 20},
        "status": "draft"
    }

def test_successful_initialization(valid_budget_data):
    budget = Budget(**valid_budget_data)
    assert budget.budget_id == "B001"
    assert budget.name == "Marketing Budget"
    assert budget.status == "draft"

def test_invalid_budget_id_raises_value_error(valid_budget_data):
    valid_budget_data["budget_id"] = ""
    with pytest.raises(ValueError, match="Budget ID must be a valid non-empty string."):
        Budget(**valid_budget_data)

def test_invalid_date_order_raises_value_error(valid_budget_data):
    valid_budget_data["start_date"] = date.today() + timedelta(days=10)
    valid_budget_data["end_date"] = date.today()
    with pytest.raises(ValueError, match="End date must be greater than start date."):
        Budget(**valid_budget_data)

def test_invalid_allocation_sum_raises_value_error(valid_budget_data):
    valid_budget_data["allocation_rule"] = {"ads": 40, "events": 30}
    with pytest.raises(ValueError, match="Allocation rule percentages must sum to 100%"):
        Budget(**valid_budget_data)

def test_update_status_transitions(valid_budget_data):
    budget = Budget(**valid_budget_data)
    budget.update_status("approved")
    assert budget.status == "approved"
    budget.update_status("draft")
    assert budget.status == "draft"

def test_invalid_status_transition_raises_value_error(valid_budget_data):
    budget = Budget(**valid_budget_data)
    budget.update_status("approved")
    with pytest.raises(ValueError, match="Invalid status transition"):
        budget.update_status("closed")

def test_calculate_total_and_unbudgeted_amount(valid_budget_data):
    budget = Budget(**valid_budget_data)
    items = {"ads": 3000, "events": 2000}
    assert budget.calculate_total_budgeted_amount(items) == 5000
    assert budget.calculate_unbudgeted_amount(items) == 5000

def test_reallocate_budget_success(valid_budget_data):
    budget = Budget(**valid_budget_data)
    items = {"ads": 5000, "events": 3000}
    updated = budget.reallocate_budget(items, "ads", "events", 1000)
    assert updated["ads"] == 4000
    assert updated["events"] == 4000

def test_invalid_reallocation_raises_value_error(valid_budget_data):
    budget = Budget(**valid_budget_data)
    items = {"ads": 1000, "events": 1000}
    with pytest.raises(ValueError, match="Cannot reallocate more than"):
        budget.reallocate_budget(items, "ads", "events", 2000)

def test_protect_attribute_modification_raises_attribute_error(valid_budget_data):
    budget = Budget(**valid_budget_data)
    with pytest.raises(AttributeError, match="Direct modification of '_name' is not allowed"):
        budget._name = "New Name"

def test_sanitize_name_raises_value_error():
    with pytest.raises(ValueError):
        Budget("id", "", date.today(), date.today() + timedelta(days=1), 1000, {"x": 100})

def test_duplicate_budget_creates_new_instance(valid_budget_data):
    budget = Budget(**valid_budget_data)
    duplicate = budget.duplicate_budget("B002", "Copy Budget")
    assert duplicate.budget_id == "B002"
    assert duplicate.name == "Copy Budget"
    assert duplicate.start_date == budget.start_date
    assert duplicate.end_date == budget.end_date
    assert duplicate.budget_allocated_amount == budget.budget_allocated_amount
    assert duplicate.allocation_rule == budget.allocation_rule
    assert duplicate.status == budget.status
    assert duplicate is not budget

def test_invalid_allocation_rule_type_raises_value_error(valid_budget_data):
    valid_budget_data["allocation_rule"] = [("ads", 50), ("events", 50)]
    with pytest.raises(ValueError, match="Allocation rule must be a dictionary."):
        Budget(**valid_budget_data)

def test_negative_allocated_amount_raises_value_error(valid_budget_data):
    valid_budget_data["budget_allocated_amount"] = -100
    with pytest.raises(ValueError, match="Allocated amount must be a positive number."):
        Budget(**valid_budget_data)

def test_invalid_status_raises_value_error(valid_budget_data):
    valid_budget_data["status"] = "pending"
    with pytest.raises(ValueError, match="Status must be 'draft', 'approved', or 'closed'."):
        Budget(**valid_budget_data)

def test_calculate_total_budgeted_amount_type_error(valid_budget_data):
    budget = Budget(**valid_budget_data)
    with pytest.raises(ValueError, match="Budgeted items must be a dictionary of {item: amount}."):
        budget.calculate_total_budgeted_amount([("ads", 1000)])

def test_calculate_unbudgeted_amount_type_error(valid_budget_data):
    budget = Budget(**valid_budget_data)
    with pytest.raises(ValueError, match="Budgeted items must be a dictionary of {item: amount}."):
        budget.calculate_unbudgeted_amount([("ads", 1000)])

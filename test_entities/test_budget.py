import pytest
from datetime import date, timedelta
from copy import deepcopy
from entities.Budget import Budget


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

def test_invalid_budget_id(valid_budget_data):
    valid_budget_data["budget_id"] = ""
    with pytest.raises(ValueError, match="Budget ID must be a valid non-empty string."):
        Budget(**valid_budget_data)

def test_invalid_date_order(valid_budget_data):
    valid_budget_data["start_date"] = date.today() + timedelta(days=10)
    valid_budget_data["end_date"] = date.today()
    with pytest.raises(ValueError, match="End date must be greater than start date."):
        Budget(**valid_budget_data)

def test_invalid_allocation_sum(valid_budget_data):
    valid_budget_data["allocation_rule"] = {"ads": 40, "events": 30}
    with pytest.raises(ValueError, match="Allocation rule percentages must sum to 100%"):
        Budget(**valid_budget_data)

def test_update_status(valid_budget_data):
    budget = Budget(**valid_budget_data)
    budget.update_status("approved")
    assert budget.status == "approved"
    budget.update_status("draft")
    assert budget.status == "draft"

def test_invalid_status_transition(valid_budget_data):
    budget = Budget(**valid_budget_data)
    budget.update_status("approved")
    with pytest.raises(ValueError, match="Invalid status transition"):
        budget.update_status("closed")

def test_calculate_total_and_unbudgeted_amount(valid_budget_data):
    budget = Budget(**valid_budget_data)
    items = {"ads": 3000, "events": 2000}
    assert budget.calculate_total_budgeted_amount(items) == 5000
    assert budget.calculate_unbudgeted_amount(items) == 5000

def test_reallocate_budget(valid_budget_data):
    budget = Budget(**valid_budget_data)
    items = {"ads": 5000, "events": 3000}
    updated = budget.reallocate_budget(items, "ads", "events", 1000)
    assert updated["ads"] == 4000
    assert updated["events"] == 4000

def test_invalid_reallocation(valid_budget_data):
    budget = Budget(**valid_budget_data)
    items = {"ads": 1000, "events": 1000}
    with pytest.raises(ValueError, match="Cannot reallocate more than"):
        budget.reallocate_budget(items, "ads", "events", 2000)

def test_protect_attribute_modification(valid_budget_data):
    budget = Budget(**valid_budget_data)
    with pytest.raises(AttributeError, match="Direct modification of '_name' is not allowed"):
        budget._name = "New Name"

def test_sanitize_name():
    with pytest.raises(ValueError):
        Budget("id", "", date.today(), date.today() + timedelta(days=1), 1000, {"x": 100})

import pytest
from datetime import date, timedelta
from entities.BudgetedItem import BudgetedItem


@pytest.fixture
def valid_budgeted_item_data():
    return {
        "name": "Groceries",
        "description": "Monthly grocery shopping",
        "amount": 300.00,
        "category": "Needs",
        "tags": ["food", "essentials"]
    }

def test_item_id_is_string_uuid(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    assert isinstance(item.item_id, str)

def test_item_id_is_unique(valid_budgeted_item_data):
    item1 = BudgetedItem(**valid_budgeted_item_data)
    item2 = BudgetedItem(**valid_budgeted_item_data)
    assert item1.item_id != item2.item_id, "item_id should be unique per instance"

def test_successful_initialization(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    assert item.name == "Groceries"
    assert item.amount == 300.00
    assert item.category == "Needs"
    assert item.tags == ["food", "essentials"]

def test_invalid_name(valid_budgeted_item_data):
    valid_budgeted_item_data["name"] = ""
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        BudgetedItem(**valid_budgeted_item_data)

def test_invalid_amount(valid_budgeted_item_data):
    valid_budgeted_item_data["amount"] = -50.00
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        BudgetedItem(**valid_budgeted_item_data)

def test_invalid_category(valid_budgeted_item_data):
    valid_budgeted_item_data["category"] = ""
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        BudgetedItem(**valid_budgeted_item_data)

def test_update_item(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    item.update_item(name="Weekly Groceries", amount=250.00, tags=["food", "weekly"])
    assert item.name == "Weekly Groceries"
    assert item.amount == 250.00
    assert item.tags == ["food", "weekly"]

def test_update_item_invalid_amount(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Amount must be greater than 0."):
        item.update_item(amount=-100.00)

def test_update_item_invalid_category(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Category cannot be empty."):
        item.update_item(category="")

def test_repr_method(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    expected_repr = (f"BudgetedItem(item_id='{item.item_id}', name='Groceries', "
                     f"description='Monthly grocery shopping', amount=300.0, "
                     f"category='Needs', tags=['food', 'essentials'])")
    assert repr(item) == expected_repr

def test_duplicate_budgeted_item(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    new_item = BudgetedItem(name=item.name, description=item.description, amount=item.amount,
                            category=item.category, tags=item.tags)
    assert new_item.item_id != item.item_id, "Duplicate item should have a different item_id"
    assert new_item.name == item.name
    assert new_item.amount == item.amount
    assert new_item.category == item.category
    assert new_item.tags == item.tags

def test_update_item_with_none(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    item.update_item(name=None, description=None, amount=None, category=None, tags=None)
    assert item.name == "Groceries"
    assert item.description == "Monthly grocery shopping"
    assert item.amount == 300.00
    assert item.category == "Needs"
    assert item.tags == ["food", "essentials"]

def test_update_item_with_empty_tags(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    item.update_item(tags=[])
    assert item.tags == [], "Tags should be updated to an empty list"
    assert item.name == "Groceries"
    assert item.amount == 300.00
    assert item.category == "Needs"
    assert item.description == "Monthly grocery shopping"

def test_update_item_with_none_tags(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    item.update_item(tags=None)
    assert item.tags == [], "Tags should default to an empty list when set to None"
    assert item.name == "Groceries"
    assert item.amount == 300.00
    assert item.category == "Needs"
    assert item.description == "Monthly grocery shopping"

def test_update_item_with_empty_name(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(name="")

def test_update_item_with_none_name(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(name=None)

def test_update_item_with_none_description(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    item.update_item(description=None)
    assert item.description == "Monthly grocery shopping", "Description should remain unchanged if set to None"
    assert item.name == "Groceries"
    assert item.amount == 300.00
    assert item.category == "Needs"
    assert item.tags == ["food", "essentials"]

def test_update_item_with_empty_description(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(description="")

def test_update_item_with_none_amount(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Amount must be greater than 0."):
        item.update_item(amount=None)

def test_update_item_with_zero_amount(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(amount=0.00)

def test_update_item_with_negative_amount(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(amount=-100.00)

def test_update_item_with_none_category(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(category=None)

def test_update_item_with_empty_category(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(category="")

def test_update_item_with_invalid_tags(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(tags="not_a_list")  # Tags should be a list, not a string

def test_update_item_with_invalid_category(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(category=123)  # Category should be a string, not an integer

def test_update_item_with_invalid_amount_type(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(amount="three hundred")  # Amount should be a float, not a string

def test_update_item_with_invalid_tags_type(valid_budgeted_item_data):
    item = BudgetedItem(**valid_budgeted_item_data)
    with pytest.raises(ValueError, match="Invalid BudgetedItem: All fields must be valid and amount must be > 0."):
        item.update_item(tags=123)  # Tags should be a list, not an integer


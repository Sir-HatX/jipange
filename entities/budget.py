class Budget:
    def __init__(self, name:str, total_amount: float, start_date: datetime, end_date:datetime, allocation_rule: dict):
        self.name = name
        self.total_amount = total_amount
        self.start_date = start_date
        self.end_date = end_date
        self.expenses = []
        self.budgeted_items = []
        self.status = 'open'
        self.allocation_rule = allocation_rule

    def add_budgeted_item(self,name:str, description:str, amount: float, category:str, tags[]):
        item = BudgetedItem(name, description, amount, category, tags)
        self.budgeted_items.append(item)
        return item
    



Budget.add_budgeted_item(description="Rent", amount=1200, category="needs")

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

        def 

        if sum(allocation_rule.values()) != 100:
            raise ValueError("Allocation rule percentages must add up to 100")
        
    def add_expense(self, expense):
        if expense.amount <= self.get_remaining_balance()
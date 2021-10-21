class User():
    def __init__(self, name, state, monthly_income):
        self.name = name
        self.state = state
        self.monthly_income = monthly_income
    
    def _get_name(self):
        return self.name
    
    def _get_state(self):
        return self.state

    def _get_monthly_income(self):
        return self.monthly_income

    def __str__(self):
        return f"{self.name} lives in {self.city} and makes {self.monthly_income} monthly."

class User():
    def __init__(self, name, city, monthly_income):
        self.name = name
        self.city = city
        self.monthly_income = monthly_income
    
    def _get_name(self):
        return self.name
    
    def _get_city(self):
        return self.city

    def _get_monthly_income(self):
        return self.monthly_income

    def __str__(self):
        return f"{self.name} lives in {self.city} and makes {self.monthly_income} monthly."

class StateInfo:
    def __init__(self, information):
        self.information = information

    def _get_name(self):
        return self.information["State"]

    def _get_cost_index(self):
        return self.information["costIndex"]

    def _get_grocery_cost(self):
        return self.information["groceryCost"]

    def _get_housing_cost(self):
        return self.information["housingCost"]

    def _get_utilities_cost(self):
        return self.information["utilitiesCost"]
    
    def _get_transportation_cost(self):
        return self.information["transportationCost"]

    def _get_misc_cost(self):
        return self.information["miscCost"]

    def __str__(self):
        gn = f"State - {self.information['State']}\n"
        ci = f"Cost Index - {self.information['costIndex']}\n"
        gc = f"Grocery Cost - {self.information['groceryCost']}\n"
        hc = f"Housing Cost - {self.information['housingCost']}\n"
        uc = f"Utilities Cost - {self.information['utilitiesCost']}\n"
        tc = f"Transportation Cost - {self.information['transportationCost']}\n"
        mc = f"Misc Cost - {self.information['miscCost']}\n"
        return f"\n{gn}{ci}{gc}{hc}{uc}{tc}{mc}"



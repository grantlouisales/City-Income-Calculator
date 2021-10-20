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

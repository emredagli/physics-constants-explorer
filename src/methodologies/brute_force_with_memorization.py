from itertools import product

from src.methodologies.brute_force import BruteForce
from src.quantity import Quantity


class BruteForceWithMemorization(BruteForce):

    def __init__(self, target, scope, settings):
        super().__init__(target, scope, settings)
        self.powered_quantities = self.get_grouped_quantities()

    def find_matched(self):
        super().find_matched()

    def get_grouped_quantities(self):
        result = []

        # Step 1 Sort by len
        list_of_powered_quantities = self.scope.get_list_of_powered_quantities()
        list_of_powered_quantities.sort(key=len, reverse=True)

        group_max_multiplication_length = 1
        if len(list_of_powered_quantities) >= 2:
            group_max_multiplication_length = len(list_of_powered_quantities[0]) * len(list_of_powered_quantities[1])

        # Step 2, prepare sub-quantities by max length
        curr_multiplication = 1
        sub_quantities = []
        max_index = len(list_of_powered_quantities) - 1
        for index, quantities in enumerate(list_of_powered_quantities):
            sub_quantities.append(quantities)
            curr_multiplication *= len(quantities)

            if index + 1 <= max_index:
                if curr_multiplication * len(list_of_powered_quantities[index + 1]) > group_max_multiplication_length:
                    result.append(self.get_merged_sub_quantities(sub_quantities))
                    curr_multiplication = 1
                    sub_quantities = []

        if len(sub_quantities) > 0:
            result.append(self.get_merged_sub_quantities(sub_quantities))

        return result

    @staticmethod
    def get_merged_sub_quantities(curr_quantities):
        result = []
        for product_result in product(*curr_quantities):
            merged_quantity = Quantity(value=list(product_result))
            result.append(merged_quantity)
        return result

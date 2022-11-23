import collections
import operator
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.quantity import Quantity



class DimensionalOperator:
    def __init__(self, method, scope, target, dimensionless_numeric_range, unit_registry):
        self.scope = scope
        self.method = method
        self.ur = unit_registry
        self.target = target
        self.dimensionless_numeric_range = dimensionless_numeric_range
        self.matched = dict()

    def _find_matched_by_brute_force(self, powered_quantities):
        total_len = reduce(operator.mul, map(len, powered_quantities), 1)
        matched = dict()
        target_dimensionality = self.target.unit.dimensionality
        for quantities in tqdm(product(*powered_quantities),
                               desc=f"Combinations of physical constants are being searched...",
                               unit=" Iteration",
                               total=total_len):
            resultant_unit = self.multiply_quantity_units(quantities)

            if resultant_unit == target_dimensionality:
                quantity = Quantity(value=list(quantities), unit_registry=self.ur)
                matched.setdefault(quantity.value, quantity)
        self.matched = collections.OrderedDict(sorted(matched.items()))

    def _find_matched_by_brute_force_with_memorization(self):
        grouped_quantities = self.scope.get_grouped_quantities(group_max_multiplication_length=1000)
        self._find_matched_by_brute_force(grouped_quantities)

    @staticmethod
    def multiply_quantity_units(quantities):
        units = [q.unit.dimensionality for q in quantities]
        return reduce(operator.mul, units[1:], units[0])

    def find_matched_multiplications(self):
        if self.method == "brute_force":
            self._find_matched_by_brute_force(self.scope.powered_quantities.values())
        elif self.method == "brute_force_with_memorization":
            self._find_matched_by_brute_force_with_memorization()
        else:
            raise ValueError("Search method (config.method) is invalid!")

        if len(self.matched.items()) == 0:
            print("Could not find physical constants combination that is matched target's unit!")

    def print_matched_results(self):
        match_count = len(self.matched.items())
        if match_count > 0:
            print(f"Found {match_count} candidates the resultant unit matched with the target's unit:")
            for expression in self.matched.values():
                # TODO Change M symbol to Q -> Quantity
                print(f"\t{{ Q }} [ {expression.get_unit_str()} ] = {expression.get_expression_with_solidus()}")
                print(f"{self.get_candidate_value_info(expression.value)}")

    # TODO: do not refactor the following part as well!
    def get_candidate_value_info(self, candidate_value):
        dimensionless_min, dimensionless_max = self.dimensionless_numeric_range
        ratio_max = self.target.value / dimensionless_min
        ratio_min = self.target.value / dimensionless_max
        ratio_max_info = f" Max (~{ratio_max:.0E}) "
        ratio_min_info = f" Min (~{ratio_min:.0E}) "
        quantity_info = f" Q (~{candidate_value:.0E}) "
        in_range_info = "👎 Not in range."
        if candidate_value > ratio_min:
            if candidate_value < ratio_max:
                in_range_info = "👍 In range!"
                quantity_info = f"{ratio_min_info}<{quantity_info}<{ratio_max_info}"
            else:
                quantity_info = f"{ratio_min_info}<{ratio_max_info}<{quantity_info}"
        else:
            quantity_info = f"{quantity_info}<{ratio_min_info}<{ratio_max_info}"

        return f"\t  ├── {in_range_info}\n" \
               f"\t  └── {quantity_info}\n"



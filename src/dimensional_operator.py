import collections
import operator
from enum import Enum
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.quantity import Quantity


class NumericPosition(Enum):
    IN_RANGE = 0
    LEFT = -1
    RIGHT = 1


class DimensionalOperator:

    def __init__(self, method, scope, target, dimensionless_numeric_range):
        self.scope = scope
        self.method = method
        self.target = target
        self.dimensionless_numeric_range = dimensionless_numeric_range
        self.candidates = dict()
        self.candidates_in_range = dict()

    def _find_matched_by_brute_force(self, powered_quantities):
        total_len = reduce(operator.mul, map(len, powered_quantities), 1)
        candidates = dict()
        candidates_in_range = dict()
        target_dimensionality = self.target.unit.dimensionality
        for quantities in tqdm(product(*powered_quantities),
                               desc=f"Combinations of dimensional constants are being searched...",
                               unit=" Iteration",
                               total=total_len):

            units = [q.unit.dimensionality for q in quantities]
            resultant_unit = reduce(operator.mul, units[1:], units[0])

            if resultant_unit == target_dimensionality:
                quantity = Quantity(value=list(quantities))
                candidates.setdefault(quantity.value, quantity)
                position, _, _ = self._dimensionless_numeric_range_position(quantity.value)
                if position == NumericPosition.IN_RANGE:
                    candidates_in_range.setdefault(quantity.value, quantity)

        self.candidates = collections.OrderedDict(sorted(candidates.items()))
        self.candidates_in_range = collections.OrderedDict(sorted(candidates_in_range.items()))

    def _find_matched_by_brute_force_with_memorization(self):
        grouped_quantities = self.scope.get_grouped_quantities()
        self._find_matched_by_brute_force(grouped_quantities)

    def explore_constant(self):
        if self.method == "brute_force":
            self._find_matched_by_brute_force(self.scope.powered_quantities.values())
        elif self.method == "brute_force_with_memorization":
            self._find_matched_by_brute_force_with_memorization()
        else:
            raise ValueError("Search method (config.method) is invalid!")

        if len(self.candidates.items()) == 0:
            print("Could not find a candidate that has the same unit as the targets!")

    def print_the_candidates(self):
        match_count = len(self.candidates.items())
        if match_count > 0:
            print(f"Found {match_count} candidates the resultant unit matched with the target's unit:")
            for expression in self.candidates.values():
                print(f"\t{{ Q }} [ {expression.get_unit_str()} ] = {expression.get_expression_with_solidus()}")
                print(f"{self.get_candidate_value_info(expression.value)}")

    def _dimensionless_numeric_range_position(self, candidate_numeric_value):
        dimensionless_min, dimensionless_max = self.dimensionless_numeric_range
        ratio_max = self.target.value / dimensionless_min
        ratio_min = self.target.value / dimensionless_max

        if candidate_numeric_value > ratio_min:
            if candidate_numeric_value < ratio_max:
                position = NumericPosition.IN_RANGE
            else:
                position = NumericPosition.RIGHT
        else:
            position = NumericPosition.LEFT

        return position, ratio_min, ratio_max

    def get_candidate_value_info(self, candidate_numeric_value):
        position, ratio_min, ratio_max = self._dimensionless_numeric_range_position(candidate_numeric_value)
        ratio_max_info = f" Max (~{ratio_max:.0E}) "
        ratio_min_info = f" Min (~{ratio_min:.0E}) "
        quantity_info = f" Q (~{candidate_numeric_value:.0E}) "
        in_range_info = "👎 Not in range."

        if position == NumericPosition.IN_RANGE:
            in_range_info = "👍 In range!"
            quantity_info = f"{ratio_min_info}<{quantity_info}<{ratio_max_info}"
        elif position == NumericPosition.RIGHT:
            quantity_info = f"{ratio_min_info}<{ratio_max_info}<{quantity_info}"
        else:
            quantity_info = f"{quantity_info}<{ratio_min_info}<{ratio_max_info}"

        return f"\t  ├── {in_range_info}\n" \
               f"\t  └──{quantity_info}\n"

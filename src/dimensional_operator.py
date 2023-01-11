from collections import OrderedDict
from enum import Enum

from src.methodologies.base_methodology import BaseMethodology
from src.methodologies.brute_force import BruteForce
from src.methodologies.brute_force_with_memorization import BruteForceWithMemorization
from src.methodologies.buckingham_pi import BuckinghamPI


class NumericPosition(Enum):
    IN_RANGE = 0
    LEFT = -1
    RIGHT = 1


class DimensionalOperator:
    methodology: BaseMethodology = None
    candidates: OrderedDict = None
    _candidates_in_range: OrderedDict = None

    def __init__(self, settings, scope, target, dimensionless_numeric_range):
        self.scope = scope
        self.settings = settings
        self.target = target
        self.dimensionless_numeric_range = dimensionless_numeric_range
        self._set_methodology()

    @property
    def candidates(self):
        if self.methodology is None:
            return None

        return self.methodology.candidates

    @property
    def candidates_in_range(self):
        if self._candidates_in_range is not None:
            return self._candidates_in_range

        if self.candidates is None:
            return None

        self._candidates_in_range = OrderedDict()
        for key, item in self.candidates.items():
            position, _, _ = self._dimensionless_numeric_range_position(item.value)
            if position == NumericPosition.IN_RANGE:
                self._candidates_in_range.setdefault(key, item)

        return self._candidates_in_range

    def _set_methodology(self):
        # TODO: is there way to use dot notation of validated jsonschema object?
        if self.settings.get("method") == "buckingham_pi":
            self.methodology = BuckinghamPI(target=self.target, scope=self.scope, settings=self.settings)
        elif self.settings.get("method") == "brute_force":
            self.methodology = BruteForce(target=self.target, scope=self.scope, settings=self.settings)
        elif self.settings.get("method") == "brute_force_with_memorization":
            self.methodology = BruteForceWithMemorization(target=self.target, scope=self.scope, settings=self.settings)
        else:
            raise ValueError("Search method (config.settings.method) is invalid!")

    def explore_constant(self):
        self.methodology.find_matched()

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

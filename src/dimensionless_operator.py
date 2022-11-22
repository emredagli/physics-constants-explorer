import operator
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.expression import Expression


class DimensionlessOperator:
    def __init__(self, scope, unit_registry):
        self.scope = scope
        self.ur = unit_registry
        self.constants = dict()

        min_value = 1
        max_value = 1
        for quantities in scope.powered_quantities.values():
            value_range = [quantities[0].value, quantities[-1].value]
            max_value *= max(value_range)
            min_value *= min(value_range)

        self.min_value = min_value
        self.max_value = max_value
        self.numeric_range = [min_value, max_value]

    def is_in_range(self, value):
        return self.min_value <= value <= self.max_value

    def prepare_dimensionless_constants(self):
        powered_quantities = self.scope.powered_quantities.values()

        total_len = reduce(operator.mul, map(len, powered_quantities), 1)

        constants = dict()
        for quantities in tqdm(product(*powered_quantities),
                               desc=f"Dimensionless set is being calculated...",
                               unit=" Iteration",
                               total=total_len):
            expression = Expression(quantities=quantities)

            constants.setdefault(expression.value, expression)

        self.constants = constants

        print(f"Totally, unique {len(self.constants.items())} dimensionless multiplications are calculated!\n")
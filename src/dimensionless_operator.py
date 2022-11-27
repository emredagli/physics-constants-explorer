import operator
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.quantity import Quantity


class DimensionlessOperator:
    def __init__(self, scope):
        self.scope = scope
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

    def prepare_constants(self):
        powered_quantities = self.scope.powered_quantities.values()

        total_len = reduce(operator.mul, map(len, powered_quantities), 1)

        constants = dict()
        for quantities in tqdm(product(*powered_quantities),
                               desc=f"Dimensionless set is being calculated...",
                               unit=" Iteration",
                               total=total_len):
            quantity = Quantity(value=list(quantities))

            constants.setdefault(quantity.value, quantity)

        self.constants = constants

        print(f"Totally, unique {len(self.constants.items())} dimensionless multiplications are calculated!\n")

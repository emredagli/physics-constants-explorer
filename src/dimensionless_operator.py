import operator
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.scope import Scope
from src.quantity import Quantity


class DimensionlessOperator:
    _numeric_range: tuple = None
    scope: Scope = None

    def __init__(self, scope):
        self.scope = scope
        self.constants = dict()

    @property
    def numeric_range(self):
        if self.scope is None:
            return None

        if self._numeric_range is None:
            min_value = 1
            max_value = 1
            for powered_quantity in self.scope.powered_quantities.values():
                quantities = list(powered_quantity.values())
                value_range = [quantities[0].value, quantities[-1].value]
                max_value *= max(value_range)
                min_value *= min(value_range)

            self._numeric_range = (min_value, max_value)

        return self._numeric_range

    def prepare_constants(self):
        powered_quantities = self.scope.get_list_of_powered_quantities()

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

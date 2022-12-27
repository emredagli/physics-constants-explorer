import operator
from collections import OrderedDict
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.methodologies.base_methodology import BaseMethodology
from src.quantity import Quantity


class BruteForce(BaseMethodology):
    powered_quantities: list[list]

    def __init__(self, target, scope, settings):
        self.powered_quantities = scope.get_list_of_powered_quantities()
        super().__init__(target, scope, settings)

    def find_matched(self):
        total_len = reduce(operator.mul, map(len, self.powered_quantities), 1)
        candidates = dict()
        target_dimensionality = self.target.unit.units.dimensionality

        for quantities in tqdm(product(*self.powered_quantities),
                               desc=f"Combinations of dimensional constants are being searched...",
                               unit=" Iteration",
                               total=total_len):

            units = [q.unit.units.dimensionality for q in quantities]
            resultant_unit = reduce(operator.mul, units[1:], units[0])

            if resultant_unit == target_dimensionality:
                quantity = Quantity(value=list(quantities))
                candidates.setdefault(quantity.get_hash(), quantity)

        self.candidates = OrderedDict(sorted(candidates.items(), key=lambda pair: pair[1].value))

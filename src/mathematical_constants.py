import operator
from decimal import Decimal
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.common_library import get_symbol, get_power_range


# TODO: rename it to MathematicalOperator
class MathematicalConstants:
    def __init__(self, config, unit_registry):
        self.np = config.get("numbers_and_powers")
        self.mcp = config.get("constants_and_powers")
        self.ur = unit_registry
        self.constants = dict()
        self.min_value = None
        self.max_value = None

    def get_keys_definition(self, spacing='\n\t\t'):
        all_items = list(self.mcp.items()) + list(self.np.items())
        result = ""
        for key, power_setting in all_items:
            result += spacing + key + " ^ " + str(get_power_range(power_setting))
        return result

    def _get_decimal(self, key, power):
        ur_val = self.ur(key + "^" + str(power))
        if isinstance(ur_val, Decimal):
            return ur_val
        else:
            return ur_val.to_base_units().magnitude

    def _get_power_values(self, values):
        result = list()
        for key, power_setting in values.items():
            result.append([{
                "s": get_symbol(key, power),
                "v": self._get_decimal(key, power)
            } for power in get_power_range(power_setting)])
        return result

    def _set_bounds(self):
        min_value = None
        max_value = None

        # values = list(self.constants.keys())
        if len(self.constants.keys()) > 0:
            min_value = min(self.constants.keys())
            max_value = max(self.constants.keys())

        self.min_value = min_value
        self.max_value = max_value

    def is_in_range(self, value):
        return self.min_value <= value <= self.max_value

    def prepare_mathematical_constants(self):
        all_list = self._get_power_values(self.np) + self._get_power_values(self.mcp)
        total_len = reduce(operator.mul, map(len, all_list), 1)

        constants = dict()
        initial_obj = {"s": "", "v": Decimal("1")}
        for combination in tqdm(product(*all_list),
                                desc=f"Mathematical multiplication set is being calculated...",
                                unit=" Iteration",
                                total=total_len):
            reduced = reduce(lambda a, b: {
                "s": (a.get("s") + " " + b.get("s")).strip(),
                "v": a.get("v") * b.get("v")
            }, list(combination), initial_obj)

            constants.setdefault(reduced.get("v"), reduced.get("s"))

        self.constants = constants
        self._set_bounds()

        print(f"Totally, unique {len(self.constants.items())} mathematical multiplications are calculated & cached!")

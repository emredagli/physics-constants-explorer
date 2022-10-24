import operator
from decimal import Decimal
from functools import reduce
from itertools import product
from tqdm import tqdm
from src.common_library import get_symbol, get_power_range, get_formatted_symbol


class PhysicalConstants:
    def __init__(self, config, unit_registry):
        self.pcp = config.get("constants_and_powers")
        self.method = config.get("method")
        self.ur = unit_registry
        self.matched = dict()

    def get_keys(self):
        return list(self.pcp.keys())

    def _get_power_values(self, values):
        result = list()
        for key, max_power in values.items():
            result.append([{
                "s": get_symbol(key, power),
                "v": self.ur(key + "^" + str(power)).to_base_units().magnitude,
                "d": self.ur(key + "^" + str(power)).to_base_units().dimensionality
            } for power in get_power_range(max_power)])
        return result

    def _find_matched_by_brute_force(self, target_unit):
        power_values = self._get_power_values(self.pcp)
        total_len = reduce(operator.mul, map(len, power_values), 1)
        target_unit_dimensionality = target_unit
        matched = dict()
        dimensionless = {"d": self.ur("1 dimensionless").dimensionality}
        for combination in tqdm(product(*power_values),
                                desc=f"Combinations of physical constants are being searched...",
                                unit=" Iteration",
                                total=total_len):
            resultant_dimensionality = reduce(lambda a, b: {"d": a.get("d") * b.get("d")}, combination, dimensionless)

            if resultant_dimensionality["d"] == target_unit_dimensionality:
                resultant = reduce(lambda a, b: {
                    "s": (a.get("s") + " " + b.get("s")).strip(),
                    "v": a.get("v") * b.get("v")
                }, list(combination), {"s": "", "v": Decimal(1)})
                matched.setdefault(resultant["v"], resultant["s"])
        self.matched = matched

    def find_matched_multiplications(self, target_unit):
        if self.method == "brute_force":
            self._find_matched_by_brute_force(target_unit)
        else:
            raise ValueError("Search method (config.physical_constants.method) is invalid!")

        match_count = len(self.matched.items())
        if match_count > 0:
            print(f"Found {match_count} candidates the resultant unit matched with the target's unit:")
            for symbol in self.matched.values():
                v = self.ur(symbol).to_base_units()
                print(f"\t[ {v.u:~P} ] = [ {get_formatted_symbol(symbol)} ]")
            print("")
        else:
            print("Could not find physical constants combination that is matched target's unit!")



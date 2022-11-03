import collections
import operator
from decimal import Decimal
from functools import reduce
from itertools import product

from tqdm import tqdm

from src.common_library import get_symbol, get_power_range, get_formatted_symbol, get_decimal_with_power_10, \
    make_underlined


# TODO: rename it to PhysicalOperator
class PhysicalConstants:
    def __init__(self, config, unit_registry):
        self.pcp = config.get("constants_and_powers")
        self.method = config.get("method")
        self.ur = unit_registry
        self.matched = dict()

    def get_keys_definition(self, spacing='\n\t\t'):
        result = ""
        for key, power_setting in self.pcp.items():
            result += spacing + key + " ^ " + str(get_power_range(power_setting))
        return result

    def _get_power_values(self, values):
        result = list()
        for key, power_setting in values.items():
            result.append([{
                "s": get_symbol(key, power),
                "v": self.ur(key + "^" + str(power)).to_base_units().magnitude,
                "d": self.ur(key + "^" + str(power)).to_base_units().dimensionality
            } for power in get_power_range(power_setting)])
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
        self.matched = collections.OrderedDict(sorted(matched.items()))

    def find_matched_multiplications(self, target_unit):
        if self.method == "brute_force":
            self._find_matched_by_brute_force(target_unit)
        else:
            raise ValueError("Search method (config.physical_constants.method) is invalid!")

        if len(self.matched.items()) == 0:
            print("Could not find physical constants combination that is matched target's unit!")

    def print_matched_results(self, target, math_min, math_max):
        match_count = len(self.matched.items())
        if match_count > 0:
            print(f"Found {match_count} candidates the resultant unit matched with the target's unit:")
            for symbol in self.matched.values():
                candidate = self.ur(symbol).to_base_units()
                candidate_unit = f"{candidate.u:~P}"
                candidate_unit = candidate_unit if candidate_unit else "dimensionless"
                print(f"\t[ M ] [ {candidate_unit} ] = {get_formatted_symbol(symbol)}")
                print(f"{self.get_candidate_value_info(candidate.m, target, math_min, math_max)}")
            print("")

    def get_candidate_value_info(self, candidate_value, target, math_min, math_max):
        ratio_max = target / math_min
        ratio_min = target / math_max
        ratio_max_info = f" Max (~{get_decimal_with_power_10(ratio_max, 0)}) "
        ratio_min_info = f" Min (~{get_decimal_with_power_10(ratio_min, 0)}) "
        candidate_info = make_underlined(f"M (~{get_decimal_with_power_10(candidate_value, 0)}) ")
        in_range_info = "👎 Not in range."
        if candidate_value > ratio_min:
            if candidate_value < ratio_max:
                in_range_info = "👍 In range!"
                candidate_info = f"{ratio_min_info}< {candidate_info}<{ratio_max_info}"
            else:
                candidate_info = f"{ratio_min_info}<{ratio_max_info}< {candidate_info}"
        else:
            candidate_info = f" {candidate_info}<{ratio_min_info}<{ratio_max_info}"

        return f"\t  ├── {in_range_info}\n" \
               f"\t  └── {candidate_info}\n"

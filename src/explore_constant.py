from tqdm import tqdm

from src.common_library import get_formatted_symbol, get_value_from_scientific_notation, \
    get_suggested_physical_constants_config, get_decimal_with_power_10
from src.mathematical_constants import MathematicalConstants
from src.physical_constants import PhysicalConstants
from src.validator_library import validate_input, validate_config


class ExploreConstant:
    def __init__(self, target_value, target_unit, config, unit_registry):
        self.ur = unit_registry
        validate_input(target_value, target_unit, unit_registry)
        validate_config(config, unit_registry)

        if not target_unit.strip():
            target_unit = "dimensionless"

        self._init_target(target_value, target_unit)

        self.pc = PhysicalConstants(
            config=config.get("physical_constants"),
            unit_registry=self.ur
        )
        self.mc = MathematicalConstants(
            config=config.get("mathematical_constants"),
            unit_registry=self.ur
        )
        self.results = None

    def _is_within_the_target_error_range(self, value):
        return self.target_min <= value <= self.target_max

    def explore(self):

        print(f"Search the target:\n"
              f"\t{self.target_str}\n"
              f"in terms of the given:\n"
              f"\tphysical constants:     {self.pc.get_keys_definition()}\n"
              f"\tmathematical constants: {self.mc.get_keys_definition()}\n"
              f"by using {self.pc.method} methodology...\n")

        results = list()

        self.pc.find_matched_multiplications(self.target_dimensional.dimensionality)

        candidates_in_range = []
        if len(self.pc.matched.items()) > 0:
            self.mc.prepare_mathematical_constants()

            self.pc.print_matched_results(self.target, self.mc.min_value, self.mc.max_value)

            for pc_value, pc_symbol in tqdm(self.pc.matched.items(),
                                            desc="Iterating the candidates",
                                            leave=True):
                if self.mc.is_in_range(self.target / pc_value):
                    candidates_in_range.append(pc_symbol)
                    for mc_value, mc_symbol in tqdm(self.mc.constants.items(),
                                                    desc="Iterating the mathematical constants",
                                                    leave=False):
                        resultant = mc_value * pc_value
                        if self._is_within_the_target_error_range(resultant):
                            results.append((resultant, get_formatted_symbol(mc_symbol + " " + pc_symbol)))

        self.results = results

        # Display the results
        if len(results) > 0:
            # print("\nReduced 'physical_constants.constants_and_powers' config for candidates:\n")
            # print(f"{get_suggested_physical_constants_config(candidates_in_range)}\n")

            print(f"Result(s) matched the target:")
            print(f"\t{self.target_str}")
            for resultant, formatted_symbol in results:
                print(f"\t {get_decimal_with_power_10(resultant.quantize(self.target))} {self.unit_str} ≈ {formatted_symbol}")
        else:
            print("No results were found that matching with the target!\n")
            if len(candidates_in_range) > 0:
                print("But the following candidates were in the given mathematical range:")
                for pc_symbol in candidates_in_range:
                    print(f"\t{get_formatted_symbol(pc_symbol)}")
                # print("\nReduced 'physical_constants.constants_and_powers' config for these candidates:\n")
                # print(f"{get_suggested_physical_constants_config(candidates_in_range)}")

    def _init_target(self, target_value, target_unit):
        value = get_value_from_scientific_notation(target_value)
        self.target = value.get("value")
        self.target_error = value.get("error")
        self.target_max = value.get("max")
        self.target_min = value.get("min")
        self.target_dimensional = self.ur(str(self.target) + " " + target_unit).to_base_units()

        unit_str = f"{self.target_dimensional.u:~P}"
        self.unit_str = unit_str
        unit_str = unit_str if unit_str else "dimensionless"

        self.target_str = f"{value.get('value_with_error_str')} {unit_str}"

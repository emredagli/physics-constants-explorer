from decimal import Decimal, ROUND_DOWN
from tqdm import tqdm
from src.common_library import get_formatted_symbol
from src.mathematical_constants import MathematicalConstants
from src.physical_constants import PhysicalConstants


class ExploreConstant:
    def __init__(self, target_value, target_unit, config, unit_registry):
        self.ur = unit_registry
        self._validate_input(target_value, target_unit, config)

        if not target_unit.strip():
            target_unit = "dimensionless"

        self.target = self.ur(target_value + " " + target_unit).to_base_units()
        self.pc = PhysicalConstants(
            config=config.get("physical_constants"),
            unit_registry=self.ur
        )
        self.mc = MathematicalConstants(
            config=config.get("mathematical_constants"),
            unit_registry=self.ur
        )
        self.results = dict()

    def _validate_input(self, target_value, target_unit, config):
        try:
            target_value_str = "{:E}".format(Decimal(target_value))
            if target_value_str.replace('+', '').lower() != target_value.replace('+', '').lower():
                raise ValueError(f"{target_value} not equal to computed value {target_value_str}")
        except Exception:
            raise

        try:
            check_dimensionless = self.ur(target_unit).to_base_units() / self.ur(target_unit).to_base_units()
            if str(check_dimensionless.dimensionality) != "dimensionless":
                raise ValueError(f"unit/unit should be dimensionless, but it is {check_dimensionless.dimensionality}")
        except Exception:
            raise

        try:
            method = config.get("physical_constants").get("method")
            pcp = config.get("physical_constants").get("constants_and_powers")
            np = config.get("mathematical_constants").get("numbers_and_powers")
            mcp = config.get("mathematical_constants").get("constants_and_powers")

            if str(method) is None:
                raise ValueError("config.physical_constants.method is invalid")

            if not pcp:
                raise ValueError(
                    "Please provide at least one item under config.physical_constants.constants_and_powers")

            for key, value in pcp.items():
                self.ur(key).to_base_units()
                int(value)

            for key, value in np.items():
                Decimal(key)
                int(value)

            for key, value in mcp.items():
                if str(self.ur(key).to_base_units().dimensionality) != 'dimensionless':
                    raise ValueError(f"Mathematical constants should be dimensionless")
                int(value)

        except Exception:
            raise

    def _is_equal_to_target(self, value):
        return value.quantize(self.target.m, rounding=ROUND_DOWN) == self.target.m

    def explore(self):

        print(f"Search the target:\n"
              f"\t{self.target:~EP}\n"
              f"in terms of the given:\n"
              f"\tphysical constants:     {self.pc.get_keys()}\n"
              f"\tmathematical constants: {self.mc.get_keys()}\n"
              f"by using {self.pc.method} methodology...\n")

        results = list()

        self.pc.find_matched_multiplications(self.target.dimensionality)

        if len(self.pc.matched.items()) > 0:
            self.mc.prepare_mathematical_constants()

            for pc_value, pc_symbol in tqdm(self.pc.matched.items(),
                                            desc="Iterating the candidates",
                                            leave=True):
                if self.mc.is_in_range(self.target.m / pc_value):
                    for mc_value, mc_symbol in tqdm(self.mc.constants.items(),
                                                    desc="Iterating the mathematical constants",
                                                    leave=False):
                        resultant = mc_value * pc_value
                        if self._is_equal_to_target(resultant):
                            formula = mc_symbol + " " + pc_symbol
                            results.append((resultant, formula, get_formatted_symbol(formula)))

        self.results = results

        # Display the results
        if len(results) > 0:
            print(f"\nResults matched the target:")
            for _, _, formatted_symbol in results:
                print(f"\t{self.target:~EP} ≈ {formatted_symbol}")
        else:
            print("No results were found that matching with the target!")


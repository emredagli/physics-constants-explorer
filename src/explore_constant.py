from decimal import Decimal

from jsonschema.exceptions import ValidationError
from tqdm import tqdm
from src.common_library import get_formatted_symbol, config_schema, get_value_from_scientific_notation
from src.mathematical_constants import MathematicalConstants
from src.physical_constants import PhysicalConstants
from jsonschema import validate


class ExploreConstant:
    def __init__(self, target_value, target_unit, config, unit_registry):
        self.ur = unit_registry
        self._validate_input(target_value, target_unit, config)

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
        self.results = dict()

    def _validate_input(self, target_value, target_unit, config):
        try:
            value = get_value_from_scientific_notation(target_value)
            if value.get("value") * Decimal("0.1") < value.get("error"):
                raise ValueError(f"Target error {value.get('error')} should be less that 0.1 * {value.get('value')}")
        except Exception:
            raise

        try:
            check_dimensionless = self.ur(target_unit).to_base_units() / self.ur(target_unit).to_base_units()
            if str(check_dimensionless.dimensionality) != "dimensionless":
                raise ValueError(f"unit/unit should be dimensionless, but it is {check_dimensionless.dimensionality}")
        except Exception:
            raise

        try:
            validate(instance=config, schema=config_schema)

            pcp = config.get("physical_constants").get("constants_and_powers")
            np = config.get("mathematical_constants").get("numbers_and_powers")
            mcp = config.get("mathematical_constants").get("constants_and_powers")

            def validate_min_max(key_val, arr_val):
                if isinstance(arr_val, list):
                    if arr_val[0] > arr_val[1]:
                        raise ValidationError(f"Invalid {key_val} config value: {arr_val}. "
                                              f"List values should be in the form: [min, max] and max >= min.")

            for key, value in pcp.items():
                try:
                    self.ur(key).to_base_units()
                except Exception:
                    raise ValidationError(f"config.physical_constants.constants_and_powers.{key} is not defined under "
                                          f"the definition file. Please check the definition file under Readme.md")
                validate_min_max(key, value)

            for key, value in np.items():
                validate_min_max(key, value)

            for key, value in mcp.items():
                if str(self.ur(key).to_base_units().dimensionality) != 'dimensionless':
                    raise ValidationError(f"Mathematical constants should be dimensionless")
                validate_min_max(key, value)

        except ValidationError:
            raise
        except Exception:
            raise ValidationError(f"Config file is invalid! Please check the Readme.md")

    def _is_equal_to_target(self, value):
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

        if len(self.pc.matched.items()) > 0:
            self.mc.prepare_mathematical_constants()

            for pc_value, pc_symbol in tqdm(self.pc.matched.items(),
                                            desc="Iterating the candidates",
                                            leave=True):
                if self.mc.is_in_range(self.target / pc_value):
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
                print(f"\t{self.target_str} ≈ {formatted_symbol}")
        else:
            print("No results were found that matching with the target!")

    def _init_target(self, target_value, target_unit):
        value = get_value_from_scientific_notation(target_value)
        self.target = value.get("value")
        self.target_error = value.get("error")
        self.target_max = value.get("max")
        self.target_min = value.get("min")
        self.target_dimensional = self.ur(str(self.target) + " " + target_unit).to_base_units()

        unit_str = f"{self.target_dimensional.u:~P}"
        unit_str = unit_str if unit_str else "dimensionless"

        self.target_str = f"{value.get('value_with_error_str')} {unit_str}"

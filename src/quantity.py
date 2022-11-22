import re

from decimal import Decimal


class Quantity:
    def __init__(self, numeric_value, power, unit_registry, unit, constant_name, symbol, uncertainty=None):
        if isinstance(numeric_value, list):
            self.init_with_quantities(numeric_value)
            return

        numeric_value = numeric_value.lower()
        regex_search = re.search(r"^(?:[1-9])(?:\.\d*)?(\(\d*\))?(?:[eE][+\-]?\d+)?$", numeric_value)

        if regex_search is not None:
            value_str = numeric_value
            error_concise = "0"
            error_in_concise_form = regex_search.group(1)
            if error_in_concise_form is not None:
                value_str = numeric_value.replace(error_in_concise_form, '')
                error_concise = error_in_concise_form.replace('(', '').replace(')', '')
            elif uncertainty is not None:
                last_digits, error_concise = uncertainty
                if "e" in value_str:
                    value_str = value_str.replace("e", last_digits + "e")
                else:
                    value_str = value_str + last_digits
        else:
            raise ValueError(f"{constant_name} ({numeric_value}) is not in scientific notation.")

        power_decimal = Decimal(power.numerator) / Decimal(power.denominator)
        value = Decimal(value_str)
        delta = Decimal(error_concise) * Decimal("10") ** Decimal(value.as_tuple().exponent)
        relative_error = delta / value

        if not unit:
            unit = "dimensionless"

        q_unit = unit_registry(unit).to_base_units()
        if q_unit.magnitude != 1:
            raise ValueError(f"Magnitude of {constant_name}'s unit ({unit}) is not equal to 1.\n"
                             f"Please provide target's unit with SI base units which are:\n"
                             f"(m, s, mol, A, K, cd, kg) or empty string "" for dimensionless targets")

        self.unit = q_unit.units ** power
        self.power = power
        self.value = value ** power_decimal
        self.relative_error = relative_error * abs(power_decimal)
        # TODO converts the following 2 lines to list type!!!!
        self.constant_name = constant_name
        # TODO no need to keep symbol
        self.symbol = symbol

    def init_with_quantities(self, list_of_quantities):
        self.unit = list_of_quantities[0].unit
        self.power = list_of_quantities[0].power
        self.value = list_of_quantities[0].value
        self.relative_error = list_of_quantities[0].relative_error

        # for quantities in list_of_quantities[1:]:
        #     self.unit = q_unit.units ** power
        #     self.power = power
        #     self.value = value ** power_decimal
        #     self.relative_error = relative_error * abs(power_decimal)
        #     self.constant_name = constant_name
        #     self.symbol = symbol


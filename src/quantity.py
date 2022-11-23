import re

from decimal import Decimal


class Quantity:
    # TODO too mant input params
    def __init__(self, value, power=None, unit_registry=None, unit=None, constant_name=None, symbol=None, uncertainty=None):
        if isinstance(value, list):
            self.init_with_quantities(value, unit_registry)
            return

        value_str = value.lower()
        regex_search = re.search(r"^(?:[1-9])(?:\.\d*)?(\(\d*\))?(?:[eE][+\-]?\d+)?$", value_str)

        if regex_search is not None:
            error_concise = "0"
            error_in_concise_form = regex_search.group(1)
            if error_in_concise_form is not None:
                value_str = value_str.replace(error_in_concise_form, '')
                error_concise = error_in_concise_form.replace('(', '').replace(')', '')
            elif uncertainty is not None:
                last_digits, error_concise = uncertainty
                if "e" in value_str:
                    value_str = value_str.replace("e", last_digits + "e")
                else:
                    value_str = value_str + last_digits
        else:
            raise ValueError(f"{constant_name} ({value_str}) is not in scientific notation.")

        power_decimal = Decimal(power.numerator) / Decimal(power.denominator)
        value_decimal = Decimal(value_str)
        delta = Decimal(error_concise) * Decimal("10") ** Decimal(value_decimal.as_tuple().exponent)
        relative_error = delta / value_decimal

        if not unit:
            unit = "dimensionless"

        q_unit = unit_registry(unit).to_base_units()
        if q_unit.magnitude != 1:
            raise ValueError(f"Magnitude of {constant_name}'s unit ({unit}) is not equal to 1.\n"
                             f"Please provide target's unit with SI base units which are:\n"
                             f"(m, s, mol, A, K, cd, kg) or empty string "" for dimensionless targets")

        self.unit = q_unit.units ** power
        self.value = value_decimal ** power_decimal
        self.relative_error = relative_error * abs(power_decimal)
        self.representation = [(constant_name, symbol, power)]

    def init_with_quantities(self, list_of_quantities, unit_registry):
        self.unit = unit_registry("dimensionless").to_base_units().units
        self.value = 1
        self.relative_error = 0
        self.representation = []
        for quantity in list_of_quantities:
            self.unit *= quantity.unit
            self.value *= quantity.value
            self.relative_error += quantity.relative_error
            self.representation += quantity.representation


import re

from decimal import Decimal, ROUND_HALF_UP


class Quantity:
    _MULTIPLICATION_SYMBOL = "⋅"
    _POWER_MAP = str.maketrans({
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
        "-": "⁻", "+": "", "/": "ᐟ"})

    # TODO too mant input params
    def __init__(self, value, power=None, unit_registry=None, unit=None, constant_name=None, symbol=None,
                 uncertainty=None):
        if isinstance(value, list):
            self._init_with_quantities(value, unit_registry)
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

    def _init_with_quantities(self, list_of_quantities, unit_registry):
        self.unit = unit_registry("dimensionless").to_base_units().units
        self.value = 1
        self.relative_error = 0
        self.representation = []
        for quantity in list_of_quantities:
            self.unit *= quantity.unit
            self.value *= quantity.value
            self.relative_error += quantity.relative_error
            self.representation += quantity.representation

    def to_string(self, target=None):
        return f"{{ {self._get_numeric_value_str(target)} }} [ {self.get_unit_str()} ] = " \
               f"{self.get_expression_with_solidus()}"

    def _get_numeric_value_str(self, target=None):
        # TODO clear the following line
        if target is None:
            target = self

        def get_sign(num):
            if num >= 0:
                return "+"
            else:
                return "-"

        def concat_list(arr):
            return "".join(map(str, arr))

        if self.relative_error == 0:
            _, digits, exponent = self.value.quantize(target.value * Decimal(10) ** -3,
                                                      rounding=ROUND_HALF_UP).as_tuple()
            result_exponent = exponent + len(digits) - 1
            power_str = "" if result_exponent == 0 else "e" + get_sign(result_exponent) + str(abs(result_exponent))
            result = f"{digits[0]}.{concat_list(digits[1:])}... {power_str} (exact)"
        else:
            delta = Decimal(f"{self.relative_error * self.value:.1E}")
            _, digits_delta, exponent_delta = delta.as_tuple()
            _, digits, exponent = self.value.quantize(delta, rounding=ROUND_HALF_UP).as_tuple()

            result_exponent = exponent + len(digits) - 1
            power_str = "" if result_exponent == 0 else "e" + get_sign(result_exponent) + str(abs(result_exponent))

            delta_in_concise = "".join(map(str, digits_delta))

            result = f"{digits[0]}.{concat_list(digits[1:])}" \
                     f"({delta_in_concise}) {power_str}"

        return result

    def get_unit_str(self):
        # unit = self.get_unit()
        # if unit is None:
        #     return "dimensionless"

        result = f"{self.unit:~P}"
        return result if result else "dimensionless"

    def get_expression_with_solidus(self):
        numerator = []
        denominator = []

        for _, symbol, power in self.representation:
            if power == 0:
                continue
            power_str_abs = str(power).replace("-", "")
            quantity_item = symbol if power_str_abs == "1" else symbol + power_str_abs.translate(self._POWER_MAP)
            if power < 0:
                denominator.append(quantity_item)
            else:
                numerator.append(quantity_item)

        numerator_str = "1"
        if len(numerator) > 0:
            numerator_str = self._MULTIPLICATION_SYMBOL.join(numerator)

        if len(denominator) > 0:
            denominator_str = self._MULTIPLICATION_SYMBOL.join(denominator)
            if len(denominator) == 1:
                result = f"{numerator_str} / {denominator_str}"
            else:
                result = f"{numerator_str} / ({denominator_str})"
        else:
            result = numerator_str
        return result

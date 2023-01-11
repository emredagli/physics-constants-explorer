from decimal import Decimal
from fractions import Fraction

from src import dimensionless_unit


class Term:
    constant_name: str
    symbol: str
    power: Fraction
    is_dimensionless: bool

    def __init__(self, constant_name, symbol, power, is_dimensionless) -> None:
        self.constant_name = constant_name
        self.symbol = symbol
        self.power = power
        self.is_dimensionless = is_dimensionless


class Quantity:
    _MULTIPLICATION_SYMBOL = "⋅"
    _POWER_MAP = str.maketrans({
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
        "-": "⁻", "+": "", "/": "ᐟ"})

    def __init__(self, value, power=None, unit=None, constant_name=None, symbol=None):
        if isinstance(value, list):
            self._init_with_quantities(value)
            return

        value_str, error_concise = value

        power_decimal = Decimal(power.numerator) / Decimal(power.denominator)
        value_decimal = Decimal(value_str)
        absolute_error = Decimal(error_concise) * Decimal("10") ** Decimal(value_decimal.as_tuple().exponent)
        relative_error = absolute_error / value_decimal

        self.unit = unit ** power
        self.value = value_decimal ** power_decimal
        self.relative_error = relative_error * abs(power_decimal)
        self.terms = [] if power == 0 else [Term(
            constant_name=constant_name,
            symbol=symbol,
            power=power,
            is_dimensionless=unit.units == dimensionless_unit.units)]

    def _init_with_quantities(self, list_of_quantities):
        self.unit = dimensionless_unit
        self.value = 1
        self.relative_error = 0
        self.terms = []
        for quantity in list_of_quantities:
            self.unit *= quantity.unit
            self.value *= quantity.value
            self.relative_error += quantity.relative_error
            self.terms += quantity.terms

    def get_hash(self):
        hash_terms = [f"{term.constant_name}::{term.power}" for term in self.terms]
        return "--".join(sorted(hash_terms))

    def power_of(self, power):
        power_decimal = Decimal(power.numerator) / Decimal(power.denominator)

        self.unit = self.unit ** power
        self.value = self.value ** power_decimal
        self.relative_error = self.relative_error * abs(power_decimal)

        if power != 0:
            for term in self.terms:
                term.power *= power
        else:
            self.terms = []

    def to_string(self, target=None):
        # TODO, Using target here is confusing. Need refactoring
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
            _, digits, exponent = self.value.quantize(target.value * Decimal(10) ** -4).as_tuple()
            result_exponent = exponent + len(digits) - 1
            power_str = "" if result_exponent == 0 else "e" + get_sign(result_exponent) + str(abs(result_exponent))
            result = f"{digits[0]}.{concat_list(digits[1:])}... {power_str} (exact)"
        else:
            delta = Decimal(f"{self.relative_error * self.value:.1E}")
            _, digits_delta, exponent_delta = delta.as_tuple()
            _, digits, exponent = self.value.quantize(delta).as_tuple()

            result_exponent = exponent + len(digits) - 1
            power_str = "" if result_exponent == 0 else "e" + get_sign(result_exponent) + str(abs(result_exponent))

            delta_in_concise = "".join(map(str, digits_delta))

            result = f"{digits[0]}.{concat_list(digits[1:])}" \
                     f"({delta_in_concise}) {power_str}"

        return result

    def get_unit_str(self):
        result = f"{self.unit.units:~P}"
        return result if result else "dimensionless"

    def get_expression_with_solidus(self):
        dimensionless_terms = list(filter(lambda term: term.is_dimensionless, self.terms))
        if len(dimensionless_terms) > 0:
            dimensionless_terms.sort(key=lambda term: term.constant_name)
            dimensionless_expression = self._get_expression_with_solidus_from(dimensionless_terms)
        else:
            dimensionless_expression = None

        dimensional_terms = list(filter(lambda term: not term.is_dimensionless, self.terms))
        if len(dimensional_terms) > 0:
            dimensional_terms.sort(key=lambda term: term.constant_name)
            dimensional_expression = self._get_expression_with_solidus_from(dimensional_terms)
        else:
            dimensional_expression = None

        if dimensionless_expression is None:
            if dimensional_expression is None:
                return "1"
            else:
                return dimensional_expression
        else:
            if dimensional_expression is None:
                return dimensionless_expression
            else:
                if len(dimensionless_terms) > 1:
                    dimensionless_expression = f"({dimensionless_expression})"
                if len(dimensional_expression) > 1:
                    dimensional_expression = f"({dimensional_expression})"

                return f"{dimensionless_expression} {self._MULTIPLICATION_SYMBOL} {dimensional_expression}"

    def _get_expression_with_solidus_from(self, terms: list[Term]):
        numerator = []
        denominator = []

        for term in terms:
            if term.power == 0:
                continue
            power_str_abs = str(term.power).replace("-", "")
            quantity_item = term.symbol if power_str_abs == "1" else term.symbol + power_str_abs.translate(
                self._POWER_MAP)
            if term.power < 0:
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
        pass

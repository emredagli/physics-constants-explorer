from decimal import Decimal, ROUND_HALF_UP


def get_sign(num):
    if num >= 0:
        return "+"
    else:
        return "-"


def concat_list(arr):
    return "".join(map(str, arr))


class Expression:
    _MULTIPLICATION_SYMBOL = "⋅"
    _POWER_MAP = str.maketrans({
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
        "-": "⁻", "+": "", "/": "ᐟ"})

    def __init__(self, quantities):
        self.value = Decimal(1)
        self.relative_error = 0
        for q in quantities:
            self.value *= q.value
            self.relative_error += q.relative_error

        self.quantities = quantities

    @classmethod
    def from_expressions(cls, e1, e2):
        return cls(e1.quantities + e2.quantities)

    def to_string(self, target=None):
        return f"{{ {self.get_numeric_value_str(target)} }} [ {self.get_unit_str()} ] = " \
               f"{self.get_expression_with_solidus()}"

    def get_numeric_value_str(self, target=None):
        # TODO clear the following line
        if target is None:
            target = self

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

    def get_expression_with_solidus(self):
        numerator = []
        denominator = []

        for quantity in self.quantities:
            for representation in quantity.representation:
                symbol = representation[1]
                power = representation[2]
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

    def get_unit(self):
        if len(self.quantities) == 0:
            return None
        result = self.quantities[0].unit
        for q in self.quantities[1:]:
            result *= q.unit
        return result

    def get_unit_str(self):
        unit = self.get_unit()
        if unit is None:
            return "dimensionless"

        result = f"{unit:~P}"
        return result if result else "dimensionless"

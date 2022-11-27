from decimal import Decimal
from fractions import Fraction
from itertools import product

from src.common_library import parse_numeric_value, parse_unit
from src.quantity import Quantity


class Scope:
    _SKIP_ON_WHERE_STATEMENT = ["π", "pi"]

    def __init__(self, constants, definition, is_dimensionless):
        self.powered_quantities = dict()
        self.scope_definition = dict()
        self.is_dimensionless = is_dimensionless

        for constant_name, power_setting in constants.items():
            constant = definition.get(constant_name)
            has_definition = True
            if constant is None and is_dimensionless:
                constant = {"numeric_value": f"{Decimal(constant_name):E}"}
                has_definition = False

            quantities = []
            power_range = self._get_power_range(power_setting)
            value = parse_numeric_value(constant.get('numeric_value'))
            unit = parse_unit(constant.get('unit', 'dimensionless'))
            symbol = constant.get('symbol', constant_name)
            for power in power_range:
                quantities.append(
                    Quantity(
                        value=value,
                        constant_name=constant_name,
                        symbol=symbol,
                        power=power,
                        unit=unit
                    )
                )
            self.powered_quantities[constant_name] = quantities

            self.scope_definition[constant_name] = {
                "numeric_value_input": constant.get('numeric_value'),
                "value": value,
                "unit": unit,
                "power_range": power_range,
                "symbol": symbol,
                "info": constant.get('info'),
                "title": constant_name.replace("_", " "),
                "has_definition": has_definition
            }

    @staticmethod
    def _get_power_range(power_setting):
        if isinstance(power_setting, dict):
            """ "x_constant": {"range": [-2, 2], "step": "1/2"} """
            min_power, max_power = power_setting.get("range")
            step = power_setting.get("step", "1/1")
            numerator, denominator = list(map(int, step.split("/")))
            power_range_numerator = list(
                range(int(min_power * denominator), int(max_power * denominator) + 1, numerator))
            power_range = list(map(lambda n: Fraction(f"{n}/{denominator}"), power_range_numerator))
        elif isinstance(power_setting, list):
            """ "x_constant": [-2, 2] """
            min_power, max_power = power_setting
            power_range = list(map(Fraction, range(min_power, max_power + 1)))
        else:
            """ "x_constant": 2 """
            power_range = list(map(Fraction, range(-power_setting, power_setting + 1)))

        if Fraction(0) not in power_range:
            power_range.append(Fraction(0))
        power_range.sort()
        return power_range

    def get_summary(self, spacing='\n\t\t'):
        result = ""
        for constant_name, definition in self.scope_definition.items():
            numeric_value, _ = definition.get("value")
            symbol = definition.get("symbol")
            powers = ", ".join(map(str, definition.get("power_range")))
            unit = f"{definition.get('unit'):~P}"
            unit = f" [ {unit} ]" if unit else ""
            if self.is_dimensionless:
                result += f"{spacing}{symbol}{unit}, powers = [{powers}]"
            else:
                result += f"{spacing}{symbol} = {{ {definition.get('numeric_value_input')} }}{unit}, powers = [{powers}]"
        return result

    def get_grouped_quantities(self):
        result = []

        # Step 1 Sort by len
        quantities_values_list = list(self.powered_quantities.values())
        quantities_values_list.sort(key=len, reverse=True)

        group_max_multiplication_length = 1
        if len(quantities_values_list) >= 2:
            group_max_multiplication_length = len(quantities_values_list[0]) * len(quantities_values_list[1])

        # Step 2, prepare sub-quantities by max length
        curr_multiplication = 1
        sub_quantities = []
        max_index = len(quantities_values_list) - 1
        for index, quantities in enumerate(quantities_values_list):
            sub_quantities.append(quantities)
            curr_multiplication *= len(quantities)

            if index + 1 <= max_index:
                if curr_multiplication * len(quantities_values_list[index + 1]) > group_max_multiplication_length:
                    result.append(self.get_merged_sub_quantities(sub_quantities))
                    curr_multiplication = 1
                    sub_quantities = []

        if len(sub_quantities) > 0:
            result.append(self.get_merged_sub_quantities(sub_quantities))

        return result

    @staticmethod
    def get_merged_sub_quantities(curr_quantities):
        result = []
        for product_result in product(*curr_quantities):
            merged_quantity = Quantity(value=list(product_result))
            result.append(merged_quantity)
        return result

    def get_where_statement(self, for_constants):
        statement = ""
        for constant_name in for_constants:
            definition = self.scope_definition.get(constant_name)
            if not definition.get("has_definition"):
                continue

            symbol = definition.get("symbol")
            if any(skip_term in [symbol, constant_name] for skip_term in self._SKIP_ON_WHERE_STATEMENT):
                continue

            title = definition.get("title")
            info = definition.get("info")
            info = f", {info}" if info else ""
            statement += f"\n* {symbol}: {title}{info}"

        return statement

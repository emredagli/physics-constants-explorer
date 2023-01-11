from collections import OrderedDict
from decimal import Decimal
from fractions import Fraction

from src.common_library import parse_numeric_value, parse_unit
from src.quantity import Quantity


class Scope:

    def __init__(self, constants, definition, is_dimensionless):
        # TODO, in common it needed to check the usage of the following params
        self.powered_quantities = dict()
        self.quantities = dict()
        self.scope_definition = dict()
        self.definition = definition
        self.is_dimensionless = is_dimensionless

        for constant_name, power_setting in constants.items():
            constant = definition.get(constant_name)
            has_definition = True
            if constant is None and is_dimensionless:
                constant = {"numeric_value": f"{Decimal(constant_name):E}"}
                has_definition = False

            quantities = OrderedDict()
            power_range = self.get_power_range(power_setting)
            value = parse_numeric_value(constant.get('numeric_value'))
            unit = parse_unit(constant.get('unit', 'dimensionless'))
            symbol = constant.get('symbol', constant_name)
            # TODO: check ".powered_quantities" usages and refactor the usages based on the last changes.
            for power in power_range:
                quantities[power] = Quantity(
                    value=value,
                    constant_name=constant_name,
                    symbol=symbol,
                    power=power,
                    unit=unit
                )
            self.powered_quantities[constant_name] = quantities
            self.quantities[constant_name] = Quantity(
                value=value,
                constant_name=constant_name,
                symbol=symbol,
                power=Fraction(1),
                unit=unit
            )

            # TODO, check the following definition needing
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

    def get_list_of_powered_quantities(self):
        return [list(powered_quantity.values()) for powered_quantity in self.powered_quantities.values()]

    @staticmethod
    def get_power_range(power_setting):
        if isinstance(power_setting, dict):
            """ "constant_x": {"range": [-2, 2], "step": "1/2"} """
            min_power, max_power = power_setting.get("range")
            step = power_setting.get("step", "1/1")
            numerator, denominator = list(map(int, step.split("/")))
            power_range_numerator = list(
                range(int(min_power * denominator), int(max_power * denominator) + 1, numerator))
            power_range = list(map(lambda n: Fraction(f"{n}/{denominator}"), power_range_numerator))
        elif isinstance(power_setting, list):
            """ "constant_x": [-2, 2] """
            min_power, max_power = power_setting
            power_range = list(map(Fraction, range(min_power, max_power + 1)))
        else:
            """ "constant_x": 2 """
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
            unit = f"{definition.get('unit').units:~P}"
            unit = f" [ {unit} ]" if unit else ""
            if self.is_dimensionless:
                result += f"{spacing}{symbol}{unit}, powers = [{powers}]"
            else:
                result += f"{spacing}{symbol} = {{ {definition.get('numeric_value_input')} }}{unit}, powers = [{powers}]"
        return result

    def get_where_statement(self, constants):
        sorted_constants = list(constants)
        sorted_constants.sort()

        statement = ""
        for constant_name in sorted_constants:
            definition = self.scope_definition.get(constant_name)
            if not definition.get("has_definition"):
                continue

            symbol = definition.get("symbol")
            title = definition.get("title")
            info = definition.get("info")
            info = f", {info}" if info else ""
            statement += f"\n* {symbol}: {title}{info}"

        return statement

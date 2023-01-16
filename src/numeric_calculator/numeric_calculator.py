from decimal import Decimal
from fractions import Fraction

from common_library import parse_unit, parse_numeric_value
from src import dimensionless_unit


class NumericCalculator:
    def __init__(self, config, definition) -> None:
        self.config = config
        self.dimensional_constants = definition.get("dimensional_constants", {})
        self.dimensionless_constants = definition.get("dimensionless_constants", {})

    def calculate(self):
        numeric = Decimal(1)
        unit = dimensionless_unit
        operations = list()
        for constant_name, power in self.config.items():
            definition = self.get_constant(constant_name)
            power_fraction = Fraction(power)
            power_decimal = Decimal(power_fraction.numerator) / Decimal(power_fraction.denominator)
            numeric_value, _ = parse_numeric_value(numeric_value=definition.get("numeric_value"))
            numeric = numeric * Decimal(numeric_value) ** power_decimal
            unit = unit * parse_unit(definition.get('unit', 'dimensionless')) ** power_fraction
            symbol = definition.get("symbol", constant_name)
            operations.append(f"{symbol} ^ {power}")

        print(f"Expression  = {' * '.join(operations)}\n"
              f"Result      = {numeric:.12E} {unit.units:~P}")


    def get_constant(self, constant_name: str):
        definition = self.get_constant_from_definition(constant_name)
        if definition is None:
            return {
                "numeric_value": f"{Decimal(constant_name):E}",
                "symbol": f"{Decimal(constant_name):E}"
            }
        else:
            return definition

    def get_constant_from_definition(self, constant_name: str):
        return self.dimensional_constants.get(constant_name,
                                              self.dimensionless_constants.get(constant_name))

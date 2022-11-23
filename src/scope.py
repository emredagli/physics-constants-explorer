from decimal import Decimal
from fractions import Fraction
import copy
from itertools import product

from src.quantity import Quantity


class Scope:
    def __init__(self, constants, definition, allow_missing_definitions, unit_registry):
        self.ur = unit_registry
        self.powered_quantities = dict()
        for constant_name, power_setting in constants.items():
            constant_definition = definition.get(constant_name)
            if constant_definition is None and allow_missing_definitions:
                constant_definition = {"numeric_value": f"{Decimal(constant_name):E}"}
            quantities = []
            for power in self._get_power_range(power_setting):
                quantities.append(
                    Quantity(
                        value=constant_definition.get('numeric_value'),
                        constant_name=constant_name,
                        symbol=constant_definition.get('symbol', constant_name),
                        power=power,
                        unit_registry=self.ur,
                        unit=constant_definition.get('unit')
                    )
                )
            self.powered_quantities[constant_name] = quantities

    @staticmethod
    def _get_power_range(power_setting):
        if isinstance(power_setting, dict):
            """ "planck_constant": {"range": [-2, 2], "step": "1/2"} """
            min_power, max_power = power_setting.get("range")
            step = power_setting.get("step", "1/1")
            numerator, denominator = list(map(int, step.split("/")))
            power_range_numerator = list(
                range(int(min_power * denominator), int(max_power * denominator) + 1, numerator))
            power_range = list(map(lambda n: Fraction(f"{n}/{denominator}"), power_range_numerator))
        elif isinstance(power_setting, list):
            """ "planck_constant": [-2, 2] """
            min_power, max_power = power_setting
            power_range = list(map(Fraction, range(min_power, max_power + 1)))
        else:
            """ "planck_constant": 2 """
            power_range = list(map(Fraction, range(-power_setting, power_setting + 1)))

        if Fraction(0) not in power_range:
            power_range.append(Fraction(0))
        power_range.sort()
        return power_range

    # TODO: find a way to add its units on the summary!
    def get_summary(self, spacing='\n\t\t'):
        result = ""
        for constant_name, quantities in self.powered_quantities.items():
            symbol = quantities[0].representation[0][1]
            symbol = "" if symbol == constant_name else f" ({symbol})"
            powers = str(list(map(lambda q: str(q.representation[0][2]), quantities))).replace("'", "")
            result += f"{spacing}{constant_name}{symbol} ^ {powers}"
        return result

    def get_grouped_quantities(self, group_max_multiplication_length):
        result = []

        # Step 1 Sort by len
        quantities_values_list = list(self.powered_quantities.values())
        quantities_values_list.sort(key=len, reverse=True)

        # Step 2, shuffle reversely
        powered_quantities_shuffled_reversely = [[]] * len(quantities_values_list)
        for index, q in enumerate(quantities_values_list):
            curr_index = index * 2
            if curr_index >= len(quantities_values_list):
                break
            powered_quantities_shuffled_reversely[curr_index] = q

        for index, q in enumerate(reversed(quantities_values_list)):
            curr_index = index * 2 + 1
            if curr_index >= len(quantities_values_list):
                break
            powered_quantities_shuffled_reversely[curr_index] = q

        # Step 3, prepare limited length multiplied_quantities
        curr_multiplication = 1
        curr_quantities = []
        max_index = len(powered_quantities_shuffled_reversely) - 1
        for index, quantities in enumerate(powered_quantities_shuffled_reversely):
            curr_quantities.append(quantities)
            curr_multiplication *= len(quantities)

            if index + 1 <= max_index:
                if curr_multiplication * len(
                        powered_quantities_shuffled_reversely[index + 1]) > group_max_multiplication_length:
                    result.append(self.get_multiped_quantities(curr_quantities))
                    curr_multiplication = 1
                    curr_quantities = []

        if len(curr_quantities) > 0:
            result.append(self.get_multiped_quantities(curr_quantities))

        # Store and return the result
        return result

    def get_multiped_quantities(self, curr_quantities):
        result = []
        for product_result in product(*curr_quantities):
            new_quantity = Quantity(value=list(product_result), unit_registry=self.ur)
            result.append(new_quantity)
        return result

import logging
from decimal import getcontext, Decimal
from fractions import Fraction

import pytest

from common_library import parse_unit, parse_numeric_value
from quantity import Quantity
from src.explore_constant import ExploreConstant
from src.tests.test_library import get_test_resources

getcontext().prec = 50

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "info, numeric_values_with_power, expected_relative_error",
    [
        # The expected relative error calculation of the following test:
        #   (0.0003 / 1.0) * |1| = 3 x 10^-4
        ("single 1.", [("1.0000(3)E+5", "1")], "3.0E-4"),
        ("single 2.", [("1.00000(30)E+5", "1")], "3.0E-4"),
        ("single 3.", [("1.0000(3)E+5", "3")], "9.0E-4"),
        ("single 4.", [("1.0000(3)E+5", "1/3")], "1.0E-4"),
        ("single 5.", [("1.0000(3)E-5", "1/3")], "1.0E-4"),
        ("single 6.", [("2.000000(6)E-45", "1/3")], "1.0E-6"),
        # The expected relative error calculation of the following test:
        #   ( 3 * |1| + 3 * |1| ) x 10^-4 = ( 6 ) x 10^-4
        ("multiplication 1.", [("1.0000(3)E+5", "1"), ("1.0000(3)E+5", "1")], "6.0E-4"),
        ("multiplication 2.", [("1.0000(3)E+5", "2"), ("1.0000(3)E+5", "1/2")], "7.50E-4"),
        ("multiplication 3.", [("2.0000(3)E+5", "2"), ("2.0000(3)E+5", "1/2")], "3.750E-4"),
        # The expected relative error calculation of the following test:
        #   ( 3/2 * |11/3| + 7 * |-5/13| ) x 10^-4 = ( 23.7 ) x 10^-4
        ("multiplication 4.", [("2.0000(3)E+5", "11/3"), ("1.0000(7)E+5", "-13/5")], "2.37E-3"),
        ("multiplication, different significant, 5.", [("1.0000(1)E+5", "1"), ("1.0000000(1)E+5", "1")], "1.0010E-4"),
        ("multiplication negative power, 6.", [("1.0000(2)E+5", "-1.5"), ("1.0000(2)E+5", "-1.5")], "6.0E-4"),
        ("multiplication negative power, 7.", [("1.0000(2)E+5", "-1.5"), ("1.0000(2)E+5", "1.5")], "6.0E-4"),
        ("multiplication negative power, 8.", [("3.0000(9)E+5", "-5"), ("4.0000(2)E+5", "-2")], "1.60E-3"),
        ("multiplication 3 values, 9.", [("1.0000(1)E-42", "1"), ("1.0000(1)E+0", "1"), ("1.0000(1)E+35", "1")], "3.0E-4"),
    ]
)
@pytest.mark.parametrize("unit", ["dimensionless", "m", "kg^2/(A s)"])
def test_relative_error_of_quantities(info, numeric_values_with_power, expected_relative_error, unit):
    # GIVEN
    quantity_list = []
    for numeric_value, power in numeric_values_with_power:
        quantity_list.append(Quantity(
            value=parse_numeric_value(numeric_value),
            power=Fraction(power),
            unit=parse_unit(unit)
        ))

    # WHEN
    resultant_quantity = Quantity(quantity_list)

    # THEN
    expected = Decimal(expected_relative_error)
    relative_error = f"{resultant_quantity.relative_error.quantize(expected):E}"
    assert relative_error == expected_relative_error, \
        f"Expected relative error of {info} is {expected_relative_error}, but got {relative_error}."

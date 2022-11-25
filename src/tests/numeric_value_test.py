import logging
from decimal import getcontext, Decimal

import pytest

from src.explore_constant import ExploreConstant
from src.tests.test_library import get_test_resources

getcontext().prec = 50

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "info, numeric_value, power, error_in_concise",
    [
        ("1- power=1", "5.0000000(8)", "1", "(8)"),
    ]
)
@pytest.mark.skip(reason="Implementation has not been finished yet!")
def test_error_for_single_constant(info, numeric_value, power, error_in_concise):
    # GIVEN
    power = int(power)
    target_value = numeric_value.replace('(', '').replace(')', '') + "000"
    logger.info(f"Testing error for single constants {info}")
    definition = {
        "dimensional_constants": {
            "n": {"numeric_value": f"{numeric_value}", "unit": "m"}
        },
        "dimensionless_constants": {"x": {"numeric_value": "2.99792458e+8"}}
    }
    config = {
        "method": "brute_force",
        "dimensional_constants": {
            "n": [0, power]
        },
        "dimensionless_constants": {"x": 1}
    }

    # WHEN
    explorer = ExploreConstant(
        target_value=target_value,
        target_unit="m",
        definition=definition,
        config=config)

    explorer.explore()

    # THEN
    assert len(explorer.results) == 1, \
        f"Expected result count for {info} is 1, but got {len(explorer.results)} results"

    result = explorer.results[0][1]

    result_unit = result.get_unit_str()
    # assert result_unit == expected_unit, \
    #     f"Expected unit for {constant_name} is {expected_unit} , but got {result_unit}"
    #
    # result_expression = result.get_expression_with_solidus()
    # assert result_expression == expected_expression, \
    #     f"Expected expression for {constant_name} is {expected_expression}, but got {result_expression}"

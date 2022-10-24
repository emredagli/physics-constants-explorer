import decimal
import logging
import pytest
from decimal import Decimal, getcontext
import pint
import pathlib

from src.explore_constant import ExploreConstant

getcontext().prec = 50

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "target_value, target_unit",
    [
        ("1", "xxx"),
        ("", "m"),
        ("z", "m"),
        ("1.432FG432", "m"),
        ("1.432FG432", "m"),
        ("1.432FG432", "m"),
    ]
)
def test_physical_constants_itself(target_value, target_unit):
    logger.info(f"Testing target_value={target_value}, target_unit={target_unit}")

    config = {
        "physical_constants": {
            "method": "brute_force",
            "constants_and_powers": {
                "speed_of_light": 2,
                "planck_constant": 2,
                "boltzmann_constant": 2,
                "elementary_charge": 2,
                "vacuum_permittivity": 2,
                "electron_mass": 2
            }
        },
        "mathematical_constants": {
            "numbers_and_powers": {
                "2": 5,
                "3": 5
            },
            "constants_and_powers": {
                "pi": 5
            }
        }
    }

    unit_registry_override = str(pathlib.Path(__file__).parent.resolve()) + '/tests_definition/default_en.txt'

    # with pytest.raises(ValueError, match=r".* 123 .*"):
    with pytest.raises((ValueError, decimal.InvalidOperation)):
        explorer = ExploreConstant(
            target_value=target_value,
            target_unit=target_unit,
            config=config,
            unit_registry=pint.UnitRegistry(
                non_int_type=Decimal,
                filename=unit_registry_override))

        explorer.explore()

import decimal
import logging
import pytest
from decimal import Decimal, getcontext
import pint
import pathlib
import json

from jsonschema.exceptions import ValidationError

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
def test_invalid_target_values(target_value, target_unit):
    logger.info(f"Testing target_value={target_value}, target_unit={target_unit}")

    test_path = str(pathlib.Path(__file__).parent.resolve()) + '/test_resources'
    unit_registry_override = f"{test_path}/default_en.txt"

    # Reading config
    with open(f"{test_path}/config.json") as f:
        config = json.load(f)

    with pytest.raises((ValueError, decimal.InvalidOperation)):
        explorer = ExploreConstant(
            target_value=target_value,
            target_unit=target_unit,
            config=config,
            unit_registry=pint.UnitRegistry(
                non_int_type=Decimal,
                filename=unit_registry_override))

        explorer.explore()


@pytest.mark.parametrize(
    "config",
    [
        {},
        {"physical_constants": {}, "mathematical_constants": {}},
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "some_other", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"not_defined": 1}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 0}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": [1]}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": [1, 2, 3]}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": [5, 4]}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1.5}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {}},
            "some_other": 4
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {"a": 1}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {"2": 1.5}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {"2": {}}, "constants_and_powers": {}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {"not_defined": 1}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {"pi": 5.6}}
        },
        {
            "physical_constants": {"method": "brute_force", "constants_and_powers": {"speed_of_light": 1}},
            "mathematical_constants": {"numbers_and_powers": {}, "constants_and_powers": {"pi": [3, -2]}}
        }
    ]
)
def test_invalid_configs(config):
    logger.info(f"Testing invalid config={config}")

    test_path = str(pathlib.Path(__file__).parent.resolve()) + '/test_resources'
    unit_registry_override = f"{test_path}/default_en.txt"

    with pytest.raises(ValidationError):
        explorer = ExploreConstant(
            target_value="4.2E0",
            target_unit="m/s",
            config=config,
            unit_registry=pint.UnitRegistry(
                non_int_type=Decimal,
                filename=unit_registry_override))

        explorer.explore()

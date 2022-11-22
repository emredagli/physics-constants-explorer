import decimal
import logging
from decimal import getcontext

import pytest
from jsonschema.exceptions import ValidationError

from src.explore_constant import ExploreConstant
from src.tests.test_library import get_test_resources

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
        ("1.432", "ounce"),
        ("1.432(10)", "ounce"),
        ("1.432(10)", "yard"),
        ("1.432(10)", "mile"),
        ("1.432(10)", "calorie"),
        ("1.432(10)", "tonne"),
        ("1.432(10)", "calorie"),
        ("1.432(10)", "hour"),
        ("1.432(10)", "day"),
        ("1.432(10)", "litre")
    ]
)
def test_invalid_target_values(target_value, target_unit):
    logger.info(f"Testing target_value={target_value}, target_unit={target_unit}")

    config, definition, unit_registry = get_test_resources()

    with pytest.raises((ValueError, decimal.InvalidOperation)):
        explorer = ExploreConstant(
            target_value=target_value,
            target_unit=target_unit,
            definition=definition,
            config=config,
            unit_registry=unit_registry)

        explorer.explore()


@pytest.mark.parametrize(
    "info, definition",
    [
        ("1", {}),
        ("2", {"dimensional_constants": {}}),
        ("3", {
            "dimensional_constants": {},
            "dimensionless_constants": {}
        }),
        ("4", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {}
        }),
        ("5", {
            "dimensional_constants": {},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("6- 'unit' and 'numeric_value' must defined for dimensional constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8"}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("7- 'unit' and 'numeric_value' must defined for dimensional constants", {
            "dimensional_constants": {"c": {"unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("8- 'numeric_value' must defined for dimensionless constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"some_other_prop": "2"}}
        }),
        ("9- 'numeric_value' must defined for dimensionless constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"unit": "m"}}
        }),
        ("10- 'unit' is meaningless for dimensionless constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2", "unit": "m"}}
        }),
        ("11- 'numeric_value' must be in scientific format", {
            "dimensional_constants": {"c": {"numeric_value": "", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("12- 'numeric_value' must be in scientific format", {
            "dimensional_constants": {"c": {"numeric_value": "321", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("13- 'unit' must defined for dimensional constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": ""}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("14- Only 'numeric_value', 'symbol' and 'info' is allowed for dimensionless constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2", "some_other": "2"}}
        }),
        ("15- Only 'numeric_value', 'unit', 'symbol' and 'info' is allowed for dimensional constants", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s", "some_other": "2"}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("16- 'symbol' must be string", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s", "symbol": 1}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("17- 'info' must be string", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s", "info": 1}},
            "dimensionless_constants": {"2": {"numeric_value": "2"}}
        }),
        ("18- 'symbol' must be string", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2", "symbol": 1}}
        }),
        ("19- 'info' must be string", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2", "info": True}}
        }),
        ("20- constant not exist under the dimensional definitions", {
            "dimensional_constants": {"x": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"2": {"numeric_value": "2", "info": True}}
        }),
        ("21- constant not exist under the dimensionless definitions", {
            "dimensional_constants": {"c": {"numeric_value": "3.0e+8", "unit": "m/s"}},
            "dimensionless_constants": {"x": {"numeric_value": "2", "info": True}}
        })
    ]
)
def test_invalid_definitions(info, definition):
    logger.info(f"Testing invalid definition={definition} when {info}")

    config = {
        "method": "brute_force",
        "dimensional_constants": {"c": 1},
        "dimensionless_constants": {"2": 1}
    }
    _, _, unit_registry = get_test_resources()

    with pytest.raises(ValidationError):
        ExploreConstant(
            target_value="4.2E0",
            target_unit="m/s",
            definition=definition,
            config=config,
            unit_registry=unit_registry)


@pytest.mark.parametrize(
    "info, config",
    [
        ("1", {}),
        ("2", {"dimensional_constants": {}, "dimensionless_constants": {}}),
        ("3", {
            "method": "brute_force",
            "dimensional_constants": {},
            "dimensionless_constants": {}
        }),
        ("4", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": 1},
            "dimensionless_constants": {}
        }),
        ("5", {
            "method": "brute_force",
            "dimensional_constants": {},
            "dimensionless_constants": {"pi": 1}
        }),
        ("6", {
            "method": "brute_force",
            "dimensional_constants": {"not_defined": 1},
            "dimensionless_constants": {"pi": 1}
        }),
        ("7-range order is invalid", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": [1, 0]},
            "dimensionless_constants": {"pi": 1}
        }),
        ("8-range must have 2 numbers", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": [-3, 3, 0.5]},
            "dimensionless_constants": {"pi": 1}
        }),
        ("9-range must have 2 numbers", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": [3]},
            "dimensionless_constants": {"pi": 1}
        }),
        ("10-range must have 2 numbers", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": 3},
            "dimensionless_constants": {"pi": [1]}
        }),
        ("11-range must have 2 numbers", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": 3},
            "dimensionless_constants": {"pi": [1, 2, 0.5]}
        }),
        ("12-range must have 2 numbers", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": ["1", "2"]},
            "dimensionless_constants": {"pi": 1}
        }),
        ("13-single int", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": "2"},
            "dimensionless_constants": {"pi": 1}
        }),
        ("14-single int", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": True},
            "dimensionless_constants": {"pi": 1}
        }),
        ("15-object must have range and step", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1, 2]}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("16-object must have range and step", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"step": "1/2"}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("17-object must have valid step", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1, 2], "step": "fdds"}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("18-object must have valid step", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1, 2], "step": True}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("19-object's step property must be in string", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1, 2], "step": 1.5}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("20-object must have valid range", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1], "step": "1/3"}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("21-object must have valid range", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1, 2, 0.5], "step": "1/3"}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("22-range first value should be less than the second one", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [3, -3], "step": "1/3"}},
            "dimensionless_constants": {"pi": 1}
        }),
        ("23-range first value should be less than the second one", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": [3, -3]},
            "dimensionless_constants": {"pi": 1}
        }),
        ("24-range first value should be less than the second one", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": 1},
            "dimensionless_constants": {"pi": {"range": [3, -3], "step": "1/3"}}
        }),
        ("25-range first value should be less than the second one", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": 1},
            "dimensionless_constants": {"pi": [3, -3]}
        }),
        ("26-integer range values must be greater than 0", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": -1},
            "dimensionless_constants": {"pi": 1}
        }),
        ("27-integer range values must be greater than 0", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": 1},
            "dimensionless_constants": {"pi": -1}
        }),
        ("28-step values must be in in fraction form", {
            "method": "brute_force",
            "dimensional_constants": {"planck_constant": {"range": [1, 3], "step": "0.3333"}},
            "dimensionless_constants": {"pi": 1}
        }),
    ]
)
def test_invalid_configs(info, config):
    logger.info(f"Testing invalid config={config}")
    definition = {
        "dimensional_constants": {
            "planck_constant": {
              "numeric_value": "6.62607015e-34",
              "unit": "kg m^2/s",
              "symbol": "ℎ"
            },
        },
        "dimensionless_constants": {
            "pi": {
              "numeric_value": "3.1415926535897932384626433832795028841971693993751",
              "symbol": "π"
            },
        }
    }
    _, _, unit_registry = get_test_resources()

    with pytest.raises(ValidationError):
        ExploreConstant(
            target_value="4.2E0",
            target_unit="m/s",
            definition=definition,
            config=config,
            unit_registry=unit_registry)


def test_valid_definition_and_config():
    logger.info(f"Testing full featured valid definition and config")

    definition = {
        "dimensional_constants": {
            "speed_of_light_in_vacuum": {
                "numeric_value": "2.99792458e+8",
                "unit": "m/s",
                "symbol": "c",
                "info": "It is exact!"
            }
        },
        "dimensionless_constants": {
            "pi": {
                "numeric_value": "3.1415926535897932384626433832795028841971693993751",
                "symbol": "π",
                "info": "It is exact!"
            }
        }
    }

    config = {
        "method": "brute_force",
        "dimensional_constants": {
            "speed_of_light_in_vacuum": {"range": [-2, 3], "step": "1/3"}
        },
        "dimensionless_constants": {
            "2": [20, 21],
            "13": [-5, 5],
            "pi": 5
        }
    }
    _, _, unit_registry = get_test_resources()

    ExploreConstant(
        target_value="4.2E0",
        target_unit="m/s",
        definition=definition,
        config=config,
        unit_registry=unit_registry)

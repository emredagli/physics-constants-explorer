import logging
import pytest
from decimal import Decimal, getcontext
import pint
import pathlib

from src.explore_constant import ExploreConstant

getcontext().prec = 50

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "name, target_value, target_unit, expected",
    [
        ("Stefan–Boltzmann constant", "5.670374E-8", "kg/(s^3 K^4)",
         "2 ⋅ pi⁵ ⋅ boltzmann_constant⁴ / (3 ⋅ 5 ⋅ speed_of_light² ⋅ planck_constant³)"),
        ("Rydberg constant", "1.09737315e+7", "1/m",
         "elementary_charge⁴ ⋅ electron_mass / (2³ ⋅ speed_of_light ⋅ planck_constant³ ⋅ vacuum_permittivity²)"),
        ("Vacuum permeability (magnetic constant)", "1.256637062e-6", "m kg/(A^2 s^2)",
         "1 / (speed_of_light² ⋅ vacuum_permittivity)"),
        ("Fine structure constant", "7.29735256E-3", "",
         "elementary_charge² / (2 ⋅ speed_of_light ⋅ planck_constant ⋅ vacuum_permittivity)")
    ]
)
def test_well_known_targets(name, target_value, target_unit, expected):
    logger.info(f"Testing {name}")

    config = {
        "physical_constants": {
            "method": "brute_force",
            "constants_and_powers": {
                "speed_of_light": 4,
                "planck_constant": 4,
                "boltzmann_constant": 4,
                "elementary_charge": 4,
                "vacuum_permittivity": 2,
                "electron_mass": 2
            }
        },
        "mathematical_constants": {
            "numbers_and_powers": {
                "2": 5,
                "3": 5,
                "5": 5
            },
            "constants_and_powers": {
                "pi": 5
            }
        }
    }

    unit_registry_override = str(pathlib.Path(__file__).parent.resolve()) + '/tests_definition/default_en.txt'

    explorer = ExploreConstant(
        target_value=target_value,
        target_unit=target_unit,
        config=config,
        unit_registry=pint.UnitRegistry(
            non_int_type=Decimal,
            filename=unit_registry_override))

    explorer.explore()
    assert len(explorer.results) == 1, \
        f"Expected 1 result for {name}, but got {len(explorer.results)} results"

    first_result = explorer.results[0][2]
    assert first_result == expected, f"Expected {expected} for {name}, but got {first_result}"


@pytest.mark.parametrize(
    "name, target_value, target_unit",
    [
        ("speed_of_light", "2.99792458E+8", "m/s"),
        ("planck_constant", "6.62607015E-34", "kg m^2/s"),
        ("boltzmann_constant", "1.380649E-23", "kg m^2/(K s^2)"),
        ("elementary_charge", "1.602176634E-19", "A s"),
        ("vacuum_permittivity", "8.8541878127647313149341707111914842699353E-12", "A^2 s^4/(kg m^3)"),
        ("electron_mass", "9.10938370150E-31", "kg"),
    ]
)
def test_physical_constants_itself(name, target_value, target_unit):
    logger.info(f"Testing {name}")

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

    unit_registry_override = 'definition/default_en.txt'

    explorer = ExploreConstant(
        target_value=target_value,
        target_unit=target_unit,
        config=config,
        unit_registry=pint.UnitRegistry(
            non_int_type=Decimal,
            filename=unit_registry_override))

    explorer.explore()
    assert len(explorer.results) == 1, \
        f"Expected 1 result for {name}, but got {len(explorer.results)} results"

    first_result = explorer.results[0][2]
    assert first_result == name, f"Expected {name}, but got {first_result}"

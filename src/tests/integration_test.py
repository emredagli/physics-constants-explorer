import logging
from decimal import getcontext

import pytest

from src.explore_constant import ExploreConstant
from src.tests.test_library import get_test_resources

getcontext().prec = 50

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "constant_name, target_value, target_unit, expected_unit, expected_expressions",
    [
        ("Stefan–Boltzmann constant", "5.670374419E-8", "kg/(s^3 K^4)",
         "kg/K⁴/s³", ["2⋅π⁵⋅k⁴ / (3⋅5⋅c²⋅ℎ³)", "2⋅π⁵⋅k⁴ / (3⋅5⋅ℎ³⋅c²)"]),
        ("Rydberg constant", "1.0973731568160(21)e+7", "1/m",
         "1/m", [
             "e⁴⋅m_e / (2³⋅c⋅ℎ³⋅ε_0²)",
             "m_e⋅e⁴ / (2³⋅c⋅ℎ³⋅ε_0²)",
             "e⁴⋅m_e / (2³⋅ℎ³⋅ε_0²⋅c)",
             "e⁴⋅m_e / (2³⋅ℎ³⋅c⋅ε_0²)"]),
        ("Fine structure constant", "7.2973525693(11)E-3", "",
         "dimensionless", ["e² / (2⋅c⋅ℎ⋅ε_0)", "e² / (2⋅ℎ⋅ε_0⋅c)", "e² / (2⋅ℎ⋅c⋅ε_0)"]),
        ("Vacuum magnetic permeability", "1.25663706212(19)e-6", "m kg/(A^2 s^2)",
         "kg·m/A²/s²", ["1 / (c²⋅ε_0)", "1 / (ε_0⋅c²)"]),
        ("Molar gas constant", "8.314462618E0", "(kg m^2)/(K mol s^2)",
         "kg·m²/K/mol/s²", ["k⋅N_A", "N_A⋅k"]),
        ("Wien frequency displacement law constant", "5.878925757E+10", "1/(K s)",
         "1/K/s", ["wien_u⋅k / ℎ"]),
        ("Impedance of free space", "3.76730313668(57)E+2", "(kg m^2)/(s^3 A^2)",
         "kg·m²/A²/s³", ["1 / (c⋅ε_0)", "1 / (ε_0⋅c)"]),
        ("Josephson constant", "4.835978484E+14", "(A s^2)/(kg m^2)",
         "A·s²/kg/m²", ["2⋅e / ℎ"]),
        ("Von Klitzing constant", "2.581280745E+4", "(kg m^2)/(A^2 s^3)",
         "kg·m²/A²/s³", ["ℎ / e²"]),
    ]
)
@pytest.mark.parametrize("method", ["buckingham_pi", "brute_force", "brute_force_with_memorization"])
def test_derived_constants(constant_name, target_value, target_unit, expected_unit, expected_expressions, method):
    # GIVEN
    logger.info(f"Testing derived constants{constant_name}")

    config, definition = get_test_resources(method)

    # WHEN
    explorer = ExploreConstant(
        target_value=target_value,
        target_unit=target_unit,
        definition=definition,
        config=config)

    explorer.explore()

    # THEN
    assert len(explorer.results) == 1, \
        f"Expected result count for {constant_name} is 1, but got {len(explorer.results)} results"

    _, first_result = explorer.results[0]

    result_unit = first_result.get_unit_str()
    assert result_unit == expected_unit, \
        f"Expected unit for {constant_name} is {expected_unit} , but got {result_unit}"

    result_expression = first_result.get_expression_with_solidus()
    assert result_expression in expected_expressions, \
        f"Expected expression for {constant_name} is not in {expected_expressions}, but got {result_expression}"


@pytest.mark.parametrize(
    "constant_name, target_value, target_unit",
    [
        ("speed_of_light_in_vacuum", "2.99792458e+8", "m/s"),
        ("planck_constant", "6.62607015e-34", "kg m^2/s"),
        ("boltzmann_constant", "1.380649e-23", "kg m^2/(K s^2)"),
        ("elementary_charge", "1.602176634e-19", "A s"),
        ("vacuum_electric_permittivity", "8.8541878128e-12", "A^2 s^4/(kg m^3)"),
        ("electron_mass", "9.1093837015e-31", "kg"),
        ("avogadro_constant", "6.02214076e+23", "1/mol"),
        ("2", "2.00000000", ""),
        ("3", "3.00000000", ""),
        ("5", "5.00000000", ""),
        ("pi", "3.14159265358979323", ""),
        ("wien_u", "2.821439372122078", ""),

        # With given error
        ("speed_of_light_in_vacuum", "2.997924(42)e+8", "m/s"),
        ("planck_constant", "6.626070(42)e-34", "kg m^2/s"),
        ("boltzmann_constant", "1.3806(42)e-23", "kg m^2/(K s^2)"),
        ("elementary_charge", "1.6021766(42)e-19", "A s"),
        ("vacuum_electric_permittivity", "8.85418781(42)e-12", "A^2 s^4/(kg m^3)"),
        ("electron_mass", "9.10938370(42)e-31", "kg"),
        ("avogadro_constant", "6.022140(42)e+23", "1/mol"),
        ("2", "2.000000(42)", ""),
        ("3", "3.000000(42)", ""),
        ("5", "5.000000(42)", ""),
        ("pi", "3.141592653589793(42)", ""),
        ("wien_u", "2.8214393721220(42)", "")
    ]
)
@pytest.mark.parametrize("method", ["buckingham_pi", "brute_force", "brute_force_with_memorization"])
def test_constants_itself(constant_name, target_value, target_unit, method):
    # GIVEN
    logger.info(f"Testing constants itself {constant_name}")
    config = {
      "settings": {
          "method": method,
          "buckingham_pi_ranges": [-2, 2]
      },
      "dimensional_constants": {
        "speed_of_light_in_vacuum": 1,
        "planck_constant": 1,
        "boltzmann_constant": 1,
        "elementary_charge": 1,
        "vacuum_electric_permittivity": 1,
        "electron_mass": 1,
        "avogadro_constant": 1
      },
      "dimensionless_constants": {
        "2": 1,
        "3": 1,
        "5": 1,
        "pi": 1,
        "wien_u": 1
      }
    }
    _, definition = get_test_resources()

    # If it is a dimensionless constant and defined under the definition file
    if target_unit == "":
        constant_definition = definition.get("dimensionless_constants").get(constant_name)
        if constant_definition is not None:
            expected_expression = constant_definition.get("symbol", constant_name)
        else:
            expected_expression = constant_name
    else:
        constant_definition = definition.get("dimensional_constants").get(constant_name)
        expected_expression = constant_definition.get("symbol", constant_name)

    # WHEN
    explorer = ExploreConstant(
        target_value=target_value,
        target_unit=target_unit,
        definition=definition,
        config=config)

    explorer.explore()

    # THEN
    assert len(explorer.results) == 1, \
        f"Expected 1 result for {constant_name}, but got {len(explorer.results)} results"

    result = explorer.results[0][1]
    result_expression = result.get_expression_with_solidus()

    assert result_expression == expected_expression, \
        f"Expected expression for {constant_name} is {expected_expression}, but got {result_expression}"

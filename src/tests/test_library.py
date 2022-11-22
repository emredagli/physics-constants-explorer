import pathlib
import json
import pint
from fractions import Fraction


def get_test_resources():
    test_resources_path = str(pathlib.Path(__file__).parent.resolve()) + '/test_resources'

    # Reading config
    with open(f"{test_resources_path}/config.json") as f:
        config = json.load(f)

    # Reading definition
    with open(f"{test_resources_path}/definition.json") as f:
        definition = json.load(f)

    unit_registry = pint.UnitRegistry(
        non_int_type=Fraction,
    )

    return config, definition, unit_registry

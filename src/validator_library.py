import json
import pathlib
from fractions import Fraction

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from src import ur
from src.common_library import parse_numeric_value, parse_unit
from src.quantity import Quantity


def validate_input(target_value, target_unit):
    try:
        target = Quantity(
            value=parse_numeric_value(numeric_value=target_value, forced_absolute_error="1"),
            power=Fraction(1),
            unit=parse_unit(target_unit.strip()),
            constant_name="Target",
            symbol="Target")

        check_dimensionless = target.unit.units / ur(target_unit).to_base_units()
        if check_dimensionless.magnitude != 1 or str(check_dimensionless.dimensionality) != "dimensionless":
            raise ValueError(f"Target unit may not contain SI base units")
    except ValueError:
        raise
    except Exception:
        raise ValueError(f"Target value {target_value} or {target_unit} unit is invalid!")


def validate_definition(definition):
    with open(str(pathlib.Path(__file__).parent.resolve()) + '/resources/schema/definition_schema.json') as f:
        definition_schema = json.load(f)
    try:
        # TODO, it would be nice to validate & check:
        #   * unique symbol definitions
        #   * unit definitions, SI base units
        #   * numeric_value definitions
        #   * no duplicate quantities (checking both unit & numeric_value)
        validate(instance=definition, schema=definition_schema)
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(f"Definition file is invalid! Please check the Readme.md")


def validate_config(config, definition):
    with open(str(pathlib.Path(__file__).parent.resolve()) + '/resources/schema/config_schema.json') as f:
        config_schema = json.load(f)

    try:
        validate(instance=config, schema=config_schema)

        dimensional_constants_config = config.get("dimensional_constants")
        dimensionless_constants_config = config.get("dimensionless_constants")

        dimensional_constants_definition = definition.get("dimensional_constants")
        dimensionless_constants_definition = definition.get("dimensionless_constants")

        for key, value in dimensional_constants_config.items():
            if dimensional_constants_definition.get(key) is None:
                raise ValidationError(f"Invalid '{key}' config key.\n"
                                      f"It is not defined under the definition file 'dimensional_constants' section. "
                                      f"Please check the definition JSON file.")
            validate_range(key, value)

        for key, value in dimensionless_constants_config.items():
            if dimensionless_constants_definition.get(key) is None:
                if not is_numeric_value(key):
                    raise ValidationError(f"Invalid '{key}' config key.\n"
                                          f"It is not defined under the definition file 'dimensionless_constants' section. "
                                          f"Please check the definition JSON file.")
            validate_range(key, value)

    except ValidationError:
        raise
    except Exception:
        raise ValidationError(f"Config file is invalid! Please check the Readme.md")


def is_numeric_value(s):
    return s.replace('.', '', 1).isdigit()


def validate_range(config_key, config_value):
    if isinstance(config_value, list):
        if config_value[0] > config_value[1]:
            raise ValidationError(f"Invalid {config_key} config value: {config_value}. "
                                  f"List values should be in the form: [min, max] and max >= min.")
    elif isinstance(config_value, dict):
        range_value = config_value.get("range")
        if range_value[0] > range_value[1]:
            raise ValidationError(f"Invalid {config_key} range value: {config_value}. "
                                  f"List values should be in the form: [min, max] and max >= min.")
        step = config_value.get("step")
        if step != str(Fraction(step)):
            raise ValidationError(f"Invalid {config_key} step value: {config_value}.\n"
                                  f"Step values should be in reduced rational number form 'a/b' that:\n"
                                  f"GCD(a, b) = 1.")
    else:
        if config_value <= 0:
            raise ValidationError(f"Invalid {config_key} config value: {config_value}. "
                                  f"Range max value should be greater than 0.")

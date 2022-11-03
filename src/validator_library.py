import json
import pathlib
from decimal import Decimal

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from src.common_library import get_value_from_scientific_notation


def validate_input(target_value, target_unit, unit_registry):
    try:
        value = get_value_from_scientific_notation(target_value)
        if value.get("value") * Decimal("0.1") < value.get("error"):
            raise ValueError(f"Target error {value.get('error')} should be less that 0.1 * {value.get('value')}")

        check_dimensionless = unit_registry(target_unit).to_base_units() / unit_registry(target_unit).to_base_units()
        if str(check_dimensionless.dimensionality) != "dimensionless":
            raise ValueError(f"unit/unit should be dimensionless, but it is {check_dimensionless.dimensionality}")

    except Exception:
        raise


def validate_config(config, unit_registry):
    with open(str(pathlib.Path(__file__).parent.resolve()) + '/resources/config_schema.json') as f:
        config_schema = json.load(f)

    try:
        validate(instance=config, schema=config_schema)

        physical_constants_powers = config.get("physical_constants").get("constants_and_powers")
        numbers_and_powers = config.get("mathematical_constants").get("numbers_and_powers")
        mathematical_constants_and_powers = config.get("mathematical_constants").get("constants_and_powers")

        def validate_min_max(key_val, arr_val):
            if isinstance(arr_val, list):
                if arr_val[0] > arr_val[1]:
                    raise ValidationError(f"Invalid {key_val} config value: {arr_val}. "
                                          f"List values should be in the form: [min, max] and max >= min.")

        for key, value in physical_constants_powers.items():
            try:
                unit_registry(key).to_base_units()
            except Exception:
                raise ValidationError(f"config.physical_constants.constants_and_powers.{key} is not defined under "
                                      f"the definition file. Please check the definition file under Readme.md")
            validate_min_max(key, value)

        for key, value in numbers_and_powers.items():
            validate_min_max(key, value)

        for key, value in mathematical_constants_and_powers.items():
            if str(unit_registry(key).to_base_units().dimensionality) != 'dimensionless':
                raise ValidationError(f"Mathematical constants should be dimensionless")
            validate_min_max(key, value)

    except ValidationError:
        raise
    except Exception:
        raise ValidationError(f"Config file is invalid! Please check the Readme.md")

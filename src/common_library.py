import re
from decimal import Decimal


def get_symbol(key, power):
    if power == 0:
        return ""
    elif power == 1:
        return key
    else:
        return key + "^" + str(power)


def get_power_range(power_setting):
    if isinstance(power_setting, list):
        power_range = list(range(power_setting[0], power_setting[1] + 1))
        if 0 not in power_range:
            power_range.append(0)
        return power_range
    return list(range(-power_setting, power_setting + 1))


power_map = str.maketrans({
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "-": "⁻", "+": ""})


def get_explanation(current, number, power):
    multiplication_str = "." if current else ""

    if power == 1:
        return current + multiplication_str + str(number)

    return current + multiplication_str + str(number) + str(power).translate(power_map)


def get_formatted_symbol(symbol):
    multiplication_symbol = " ⋅ "  # or " ✕ " ?
    pairs = symbol.strip().split()
    numerator = []
    denominator = []
    for pair in pairs:
        value_pair = pair.split('^')
        if len(value_pair) == 2:
            power = int(value_pair[1])
            if power < 0:
                if power == -1:
                    denominator.append(value_pair[0])
                else:
                    denominator.append(value_pair[0] + str(abs(power)).translate(power_map))
            else:
                numerator.append(value_pair[0] + str(value_pair[1]).translate(power_map))
        else:
            numerator.append(value_pair[0])

    formatted_numerator = "1"
    if len(numerator) > 0:
        formatted_numerator = multiplication_symbol.join(numerator)

    if len(denominator) > 0:
        formatted_denominator = multiplication_symbol.join(denominator)
        if len(denominator) == 1:
            formatted = f"{formatted_numerator} / {formatted_denominator}"
        else:
            formatted = f"{formatted_numerator} / ({formatted_denominator})"
    else:
        formatted = formatted_numerator

    return formatted


def get_measurement_error_form(value, error_concise):
    sign, digits, exponent = value.as_tuple()
    error_concise_decimal = Decimal(error_concise) * Decimal(10) ** -(len(digits) - 1)
    target_str = str(digits[0]) + "." + "".join(map(str, digits[1:]))

    result_exponent = exponent + len(digits) - 1
    power_str = "" if result_exponent == 0 else "✕10" + str(result_exponent).translate(power_map)

    return f"({target_str} ± {error_concise_decimal:f}){power_str}"


def get_value_from_scientific_notation(value_str, value_name="Target Value"):
    regex_search = re.search(r"^(?:[1-9])(?:\.\d*)?(\(\d*\))?(?:[eE][+\-]?\d+)$", value_str)

    if regex_search is not None:
        error_in_concise_form = regex_search.group(1)
        if error_in_concise_form is not None:
            value_str = value_str.replace(error_in_concise_form, '')
            error_concise = error_in_concise_form.replace('(', '').replace(')', '')
        else:
            value_str = value_str.upper().replace("E", "5E")
            error_concise = "5"
    else:
        raise ValueError(f"{value_name} ({value_str}) is not in scientific notation.")

    value_decimal = Decimal(value_str)

    if value_decimal < Decimal("0"):
        raise ValueError(f"{value_name} ({value_str}) should be positive.")

    error_decimal = Decimal(error_concise) * Decimal("10") ** Decimal(value_decimal.as_tuple().exponent)

    return {
        "value": value_decimal,
        "error": error_decimal,
        "value_with_error_str": get_measurement_error_form(value_decimal, error_concise),
        "max": value_decimal + error_decimal,
        "min": value_decimal - error_decimal
    }


config_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "required": [
        "physical_constants",
        "mathematical_constants"
    ],
    "additionalProperties": False,
    "properties": {
        "physical_constants": {
            "type": "object",
            "required": [
                "method",
                "constants_and_powers"
            ],
            "additionalProperties": False,
            "properties": {
                "method": {
                    "enum": ["brute_force"],
                    "additionalProperties": False
                },
                "constants_and_powers": {
                    "type": "object",
                    "minProperties": 1,
                    "additionalProperties": {"$ref": "#/$defs/power_values"}
                }
            }
        },
        "mathematical_constants": {
            "type": "object",
            "required": [
                "numbers_and_powers",
                "constants_and_powers"
            ],
            "additionalProperties": False,
            "properties": {
                "numbers_and_powers": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9]*$": {"$ref": "#/$defs/power_values"}
                    },
                    "additionalProperties": False
                },
                "constants_and_powers": {
                    "type": "object",
                    "additionalProperties": {"$ref": "#/$defs/power_values"}
                }
            }
        },
    },
    "$defs": {
        "power_values": {
            "oneOf": [
                {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "minItems": 2,
                    "maxItems": 2,
                    "uniqueItems": False
                }, {
                    "type": "integer",
                    "minimum": 1
                }
            ]
        }
    }
}

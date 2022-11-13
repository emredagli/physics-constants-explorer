import re
from decimal import Decimal
import json


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


def make_underlined(val):
    return "\u0332".join(val)


def get_constant_with_power(constant, power):
    if constant.startswith("sqrt_") and power % 2 == 0:
        constant = constant.replace("sqrt_", "")
        power = int(power / int(2))
    if power == 1:
        return constant
    else:
        return constant + str(power).translate(power_map)


def get_formatted_symbol(symbol):
    multiplication_symbol = " ⋅ "  # or " ✕ " ?
    pairs = symbol.strip().split()
    numerator = []
    denominator = []
    for pair in pairs:
        pair_split = pair.split('^')
        constant = pair_split[0]
        if len(pair_split) < 2:
            power = "1"
        else:
            power = pair_split[1]
        power = int(power)

        if power < 0:
            if power == -1:
                denominator.append(constant)
            else:
                denominator.append(get_constant_with_power(constant, abs(power)))
        else:
            if power == 1:
                numerator.append(constant)
            else:
                numerator.append(get_constant_with_power(constant, power))

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


def get_decimal_with_power_10(value, decimal=None):
    if decimal is None:
        str_scientific = f"{value:E}"
    else:
        str_scientific = f"{value:.{decimal}E}"
    numeric_val, power_val = str_scientific.split("E")
    if power_val == 0:
        return numeric_val
    else:
        return numeric_val + "✕10" + power_val.translate(power_map)


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


def print_suggested_physical_constants_config(candidates_in_range):
    suggested_config = dict()
    for symbol in candidates_in_range:
        pairs = symbol.strip().split()
        for pair in pairs:
            pair_split = pair.split('^')
            constant = pair_split[0]
            if len(pair_split) < 2:
                power = "1"
            else:
                power = pair_split[1]
            power = int(power)
            suggested = suggested_config.get(constant)
            if suggested is None:
                suggested_config[constant] = [power, power]
            else:
                [min_val, max_val] = suggested
                suggested_config[constant] = [min(min_val, power), max(max_val, power)]
    if len(suggested_config.keys()) > 0:
        print_results = json.dumps(suggested_config, sort_keys=True).replace("],", "],\n")
        print("\nReduced 'physical_constants.constants_and_powers' config for candidates:\n")
        print(f"{print_results}\n")

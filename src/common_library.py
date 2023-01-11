import re
from decimal import Decimal, InvalidOperation

from src import ur


def parse_numeric_value(numeric_value: str, forced_absolute_error: str = None):
    formatted_numeric_value = numeric_value.strip().replace(" ", "")
    regex_search = re.search(r"^(?:[0-9]\d*)(?:\.\d*)?(\(\d*\))?(?:[eE][+\-]?\d+)?$", formatted_numeric_value)

    if regex_search is not None:
        absolute_error = "0"
        concise_error = regex_search.group(1)
        if concise_error is not None:
            formatted_numeric_value = formatted_numeric_value.replace(concise_error, '')
            absolute_error = concise_error.replace('(', '').replace(')', '')
        elif forced_absolute_error is not None:
            absolute_error = forced_absolute_error

        try:
            formatted_numeric_value = f"{Decimal(formatted_numeric_value):E}"
        except InvalidOperation:
            raise ValueError(f"({numeric_value}) is not in desired format.")
    else:
        raise ValueError(f"({numeric_value}) is not in desired format.")

    return formatted_numeric_value, absolute_error


def parse_unit(unit):
    pint_unit = ur(unit).to_base_units()
    if pint_unit.magnitude != 1:
        raise ValueError(f"Magnitude of unit ({unit}) is not equal to 1.\n"
                         f"Please provide target's unit with SI base units which are:\n"
                         f"(m, s, mol, A, K, cd, kg) or empty string "" for dimensionless targets")

    return pint_unit

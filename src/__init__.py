from fractions import Fraction

from pint import UnitRegistry, register_unit_format, formatter

_PRETTY_EXPONENTS = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def _pretty_faction_exponent(num):
    f_num = Fraction(num).limit_denominator(1000000)
    numerator = f_num.numerator
    denominator = f_num.denominator
    if denominator == 1:
        ret = f"{str(numerator)}"
    else:
        ret = f"{str(numerator)}/{str(denominator)}"

    ret = ret.replace("/", "ᐟ").replace("-", "⁻").replace(".", "\u22C5")
    for n in range(10):
        ret = ret.replace(str(n), _PRETTY_EXPONENTS[n])
    return ret


@register_unit_format("FU")
def format_pretty(unit, registry, **options):
    return formatter(
        unit.items(),
        as_ratio=True,
        single_denominator=True,
        product_fmt="·",
        division_fmt="/",
        power_fmt="{}{}",
        parentheses_fmt="({})",
        exp_call=_pretty_faction_exponent,
        **options,
    )


# Global pint unit registry instance
ur = UnitRegistry(
    non_int_type=Fraction
)

dimensionless_unit = ur("dimensionless").to_base_units().units

import os
from datetime import datetime

from pint import register_unit_format, formatter

ALL_CONSTANTS_DIRECTORY = f'{os.path.dirname(__file__)}/pages/'
ALL_CONSTANTS_LIST_FILE_PATH = f'{ALL_CONSTANTS_DIRECTORY}_all_constants_list.html'
RESULT_FILE_PATH = f'{os.path.dirname(__file__)}/extracted/codata_extracted.json'
# DEFINITION_FILE_PATH = f'{os.path.dirname(__file__)}/extracted/default_definition{datetime.now(tz=None)}.json'
DEFINITION_FILE_PATH = f'{os.path.dirname(__file__)}/extracted/default_definition.json'
DEFINITION_TEMPLATE_FILE_PATH = f'{os.path.dirname(__file__)}/resources/default_definition_template.json'


@register_unit_format("CU")
def format_custom_unit(unit, registry, **options):
    return formatter(
        unit.items(),
        as_ratio=False,
        single_denominator=False,
        product_fmt=" ",
        power_fmt="{}^{}",
        parentheses_fmt=r"({})",
        **options,
    )

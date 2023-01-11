import json
from decimal import Decimal, getcontext
from pylatexenc.latex2text import LatexNodes2Text
import pint
from bs4 import BeautifulSoup

from src.common_library import parse_numeric_value
from src.codata_extractor import RESULT_FILE_PATH, ALL_CONSTANTS_DIRECTORY, DEFINITION_FILE_PATH, \
    DEFINITION_TEMPLATE_FILE_PATH

getcontext().prec = 50

ur = pint.UnitRegistry(
    non_int_type=Decimal
)


def get_unit_def(constant_name):
    return f"{ur(constant_name).to_base_units().units:~CU}"


with open(RESULT_FILE_PATH, 'r') as f:
    constants: dict = json.load(f)

with open(DEFINITION_TEMPLATE_FILE_PATH, 'r') as f:
    default_definition: dict = json.load(f)

for index, key in enumerate(constants.keys()):
    if key.endswith('_relationship') or key.endswith('_equivalent') or "_over_" in key or "_times_" in key or "inverse_" in key:
        continue

    # " in " is used to represent the same constant in different unit (except "speed of light in vacuum")
    if "_in_" in key and "_in_vacuum" not in key:
        continue

    # Shielded ... constants are filtered
    if "shielded_" in key:
        continue

    # Skip the following list:
    if key in ["natural_unit_of_velocity"]:
        continue

    obj = constants[key]
    with open(f"{ALL_CONSTANTS_DIRECTORY}{key}.html", 'r') as f:
        content = f.readlines()
        content = "".join(content)

    key = key.replace("-", "_")

    content = content.replace("&nbsp;", " ")
    content = content.replace("<sup>", "^").replace("</sup>", "")
    content = content.replace('<img align=ABSBOTTOM alt="OmegaRed" src="/cuu/Images/OmegaRed.gif">', "ohm")
    content = content.replace('<img align=ABSBOTTOM alt="Omega" src="/cuu/Images/Omega.gif">', "ohm")

    soup = BeautifulSoup(content, "html.parser")
    concise_text = soup.select(
        'body > p > table > tr > td:nth-child(2) > table > tr:nth-child(10) > td:nth-child(2) > tt > b > font')[0]
    concise_text_split = concise_text.text.split('\t')
    numeric_value = concise_text_split[0]
    unit_value = concise_text_split[1] if len(concise_text_split) > 1 else ""

    latex_symbol = soup.select('body > p > table > tr > td:nth-child(2) > table > tr:nth-child(2) > td > b > font img')[0].attrs.get("alt")
    # A sample latex_symbol value to understand its format: ' $m_{\\rm \\alpha}$ '
    latex_symbol = latex_symbol.strip()[1:][:-1].strip() \
        .replace("\\rmss", "\\rm \\").replace("\\lbar", "\\lambdabar")

    latex_symbol_original = latex_symbol

    if "/" in latex_symbol:
        latex_symbol = f"({latex_symbol})"

    if "," in latex_symbol:
        latex_symbol = latex_symbol.split(",")[1].strip()

    if "^-" in latex_symbol:
        latex_symbol = latex_symbol.replace("^-", "")

    symbol = LatexNodes2Text().latex_to_text(latex_symbol)

    numeric_value = numeric_value.strip() \
        .replace('x 10^-', 'e-') \
        .replace('x 10^', 'e+') \
        .replace(' ', '') \
        .replace('...', '')

    unit_value = unit_value.strip()
    info = ""

    if numeric_value.startswith("-"):
        numeric_value = numeric_value[1:]
        info = "The absolute value of the constant"

    formatted_numeric_value, absolute_error = parse_numeric_value(numeric_value)

    if unit_value != "":
        collection = default_definition["dimensional_constants"]
    else:
        collection = default_definition["dimensionless_constants"]

    default_item = collection.get(key, {})
    collection[key] = {
        "name": default_item.get("name", obj["name"]),
        "numeric_value": default_item.get("numeric_value", numeric_value),
        "symbol": default_item.get("symbol", symbol),
        "latex": default_item.get("latex", latex_symbol),
        "codata": default_item.get("codata", obj["codata"]),
        # TODO comment the following values:
        # "latex_symbol_original": latex_symbol_original
    }

    if unit_value != "":
        unit_value = default_item.get("unit", unit_value)
        collection[key]["unit"] = get_unit_def(unit_value)

    if info != "":
        collection[key]["info"] = default_item.get("info", info)


def check_and_print_item(key, obj):
    unit = obj.get("unit", "")
    symbol = obj.get("symbol", "")
    latex = obj.get("latex", "")
    latex_symbol_original = obj.get("latex_symbol_original", "")
    codata = obj.get("codata", "")
    print(f"{symbol} - {key} - {latex}-> {codata}")

    if unit != "" and ur("1 " + unit).to_base_units().magnitude != Decimal(1):
        print(f"---> IMPORTANT! {index}", get_unit_def("1 " + unit))

    for replaced_symbol in ['/', ',', '^-']:
        if replaced_symbol in latex_symbol_original:
            print(f"\t---> {replaced_symbol} exist in    {latex_symbol_original}   --->    {latex}")


for constant_group in ["dimensional_constants", "dimensionless_constants"]:
    constants = default_definition.get(constant_group)
    constants_list = list(constants.items())
    constants_list.sort(key=lambda t: t[1].get("index", 0))
    print(f"---------------- {constant_group.upper()} -------------")
    for key, obj in constants_list:
        check_and_print_item(key, obj)


with open(DEFINITION_FILE_PATH, 'w', encoding='utf8') as f:
    f.write(json.dumps(default_definition, indent=2, ensure_ascii=False))

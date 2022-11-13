import argparse
import json
from argparse import RawTextHelpFormatter

import pint
from decimal import Decimal, getcontext
from src.explore_constant import ExploreConstant

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='It will search the nearest physical and mathematical\n'
                                                 'representation of the dimensional physical value target\n'
                                                 'in terms of the given scope and power ranges.',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v',
                        '--target-value',
                        required=True,
                        metavar='\b',
                        help='Target value with scientific notation.\n'
                             'To specify target value with the standard uncertainty please use "concise form".\n'
                             'For example to provide this value (1.23±0.06)×10^−5, enter "1.23(6)E-5".\n'
                             'Some examples: "1.23(6)E-5", "8.9875(15)E+16", "4.2(3)E+0"\n'
                             'The target value can also be provided without uncertainty specification:\n'
                             'In this cae, the program converts "1.23E-5" to "1.235(5)E-5"\n'
                             'Some examples: "1.23E-5", "8.9875E+16", "4.2E+0"')

    parser.add_argument('-u',
                        '--target-unit',
                        required=True,
                        metavar='\b',
                        help='Target unit expression in terms of SI base units symbols.\n'
                             'Length - meter (m)\n'
                             'Time - second (s)\n'
                             'Amount of substance - mole (mol)\n'
                             'Electric current - ampere (A)\n'
                             'Temperature - kelvin (K)\n'
                             'Luminous intensity - candela (cd)\n'
                             'Mass - kilogram (kg)\n'
                             'Please use ^ symbol to represent power and space for multiplication.\n'
                             'Some examples: "kg/(s^3 K^4)", "kg s^-3 K^-4", "m/s"')

    parser.add_argument('-c',
                        '--config-file',
                        required=False,
                        default='./src/resources/default_config.json',
                        metavar='\b',
                        help='The config file relative path.\n'
                             'It is a JSON file that contains the list of physical and mathematical constants\n'
                             'with their power ranges. This file is validated by "src/resources/config_schema.json"\n'
                             'If it is not provided the program will use default config file:\n'
                             './src/resources/default_config.json')

    parser.add_argument('-d',
                        '--definition-file',
                        required=False,
                        default=None,
                        metavar='\b',
                        help='Definition file relative path.\n'
                             'If it is not provided the program use pint library default definition file:\n'
                             'https://github.com/hgrecco/pint/blob/master/pint/default_en.txt\n'
                             'And loads default physical constant definitions:\n'
                             'https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt\n'
                             'To customize it, please copy these 2 files, make customization on constants_en.txt file\n'
                             'and reference default_en.txt relative path for this parameter.\n'
                             'Please look at the examples given on the Readme.md file'
                        )

    args = parser.parse_args()

    # Setting Decimal precision
    getcontext().prec = 50

    # Reading config
    with open(args.config_file) as f:
        config = json.load(f)

    # pint customization
    if args.definition_file is None:
        unit_registry = pint.UnitRegistry(non_int_type=Decimal)
    else:
        unit_registry = pint.UnitRegistry(non_int_type=Decimal, filename=args.definition_file)

    explorer = ExploreConstant(
        target_value=args.target_value,
        target_unit=args.target_unit,
        config=config,
        unit_registry=unit_registry)

    explorer.explore()

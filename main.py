import argparse
import json
from argparse import RawTextHelpFormatter
from decimal import getcontext
from fractions import Fraction

import pint
import src.common_library
from src.explore_constant import ExploreConstant

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='It will explore the nearest representation of the given physical quantity\n'
                                                 'in terms of the given other quantity definitions and the scope.',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v',
                        '--target-value',
                        required=True,
                        metavar='\b',
                        help='Target value with scientific notation.\n'
                             'To specify target value with the standard uncertainty please use "concise form".\n'
                             'For example to execute (1.23±0.06)×10^−5, enter "1.23(6)E-5" or "1.230(60)E-5".\n'
                             'Some valid examples: "1.23(6)E-5", "8.9875(15)E+16", "4.20(30)E+0"\n'
                             'The target value can also be provided without uncertainty specification:\n'
                             'In this cae, the program converts "1.23E-5" to "1.230(10)E-5"\n'
                             'Some valid examples: "1.23E-5", "8.9875E+16", "4.2E+0"')

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
                             'Some valid examples: "kg/(s^3 K^4)", "kg s^-3 K^-4", "m/s"')

    parser.add_argument('-c',
                        '--config-file',
                        required=False,
                        default='./src/resources/default_config.json',
                        metavar='\b',
                        help='The config file relative path.\n'
                             'It is a JSON file that contains the list of dimensional and dimensionless constants\n'
                             'with their power range. This file is validated by "src/resources/config_schema.json"\n'
                             'If it is not provided the program will use the default config file:\n'
                             './src/resources/default_config.json')

    parser.add_argument('-d',
                        '--definition-file',
                        required=False,
                        default='./src/resources/default_definition.json',
                        metavar='\b',
                        help='Definition file relative path.\n'
                             'It is a JSON file that contains the definition of dimensional and dimensionless constants.\n'
                             'This file is validated by "src/resources/definition_schema.json"\n'
                             'If it is not provided the program will use default definition file:\n'
                             './src/resources/default_definition.json'
                        )

    args = parser.parse_args()

    # Setting Decimal precision
    getcontext().prec = 50

    # Reading config
    with open(args.config_file) as f:
        config = json.load(f)

    # Reading definition
    with open(args.definition_file) as f:
        definition = json.load(f)

    # pint unit registry
    unit_registry = pint.UnitRegistry(
        non_int_type=Fraction
    )

    explorer = ExploreConstant(
        target_value=args.target_value,
        target_unit=args.target_unit,
        definition=definition,
        config=config,
        unit_registry=unit_registry)

    explorer.explore()

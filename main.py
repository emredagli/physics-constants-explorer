import argparse
import json
from argparse import RawTextHelpFormatter

import pint
from decimal import Decimal, getcontext
from src.explore_constant import ExploreConstant

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='It will search the nearest physical & mathematical representation of '
                                                 'the dimensional target physical value '
                                                 'in terms of the given scope & range.',
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
                        '--config-path',
                        required=False,
                        default='./config/config.json',
                        metavar='\b',
                        help='Config file relative path.\n'
                             'If it is not provided the program will use default config file: config/config.json')

    args = parser.parse_args()

    # Setting Decimal precision
    getcontext().prec = 50

    # Reading config
    with open(args.config_path) as f:
        config = json.load(f)

    # Enabling pint customization
    unit_registry_override = 'definition/default_en.txt'

    explorer = ExploreConstant(
        target_value=args.target_value,
        target_unit=args.target_unit,
        config=config,
        unit_registry=pint.UnitRegistry(
            non_int_type=Decimal,
            filename=unit_registry_override))

    explorer.explore()

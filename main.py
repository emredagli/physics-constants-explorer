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
                             'To specify target value with measurement error:\n '
                             'For example (1.23±0.06)×10^−5, please provide it in "concise form" like 1.23(6)E-5.\n'
                             'Examples with error: "1.23(6)E-5", "8.9875(15)E+16", "4.2(3)E+0"\n'
                             'The target can be provided without error:\n'
                             'Examples without error: "1.23E-5", "8.9875E+16", "4.2E+0"\n'
                             'If you provide without error, it is equal to:\n'
                             '"1.23E-5" ≈ "1.235(5)E-5"')

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
                             'Use ^ symbol to represent power.\n'
                             'Examples: "kg/(s^3 K^4)", "kg s^-3 K^-4", "m/s"')

    args = parser.parse_args()

    # Setting Decimal precision
    getcontext().prec = 50

    # Reading config
    with open('config.json') as f:
        config = json.load(f)

    # pint customization can be done on this file
    unit_registry_override = 'definition/default_en.txt'

    explorer = ExploreConstant(
        target_value=args.target_value,
        target_unit=args.target_unit,
        config=config,
        unit_registry=pint.UnitRegistry(
            non_int_type=Decimal,
            filename=unit_registry_override))

    explorer.explore()

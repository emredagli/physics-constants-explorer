"""
The purpose of this script is to calculate an expression which may contain some dimensional and dimensionless constants.
The constants defined on the definition file (src/resources/default_definition.json) can be used.
"""
import argparse
import json
from argparse import RawTextHelpFormatter
from decimal import getcontext, ROUND_HALF_UP

from src.numeric_calculator.numeric_calculator import NumericCalculator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Expression calculator',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c',
                        '--config-file',
                        required=False,
                        default='./src/resources/numeric_calculator/sample.json',
                        metavar='\b',
                        help='Relative path of the config file.\n'
                             'It is a JSON file that contains the list of dimensional and dimensionless constants\n'
                             'with their power values. It calculates the multiplication of the resultants.\n'
                             'The program uses the default config file to get numeric values of constants.')

    args = parser.parse_args()

    # Setting Decimal precision
    getcontext().prec = 50
    getcontext().rounding = ROUND_HALF_UP

    # Reading config
    with open(args.config_file) as f:
        config = json.load(f)

    # Reading definition
    with open('./src/resources/default_definition.json') as f:
        definition = json.load(f)

    numeric_calculator = NumericCalculator(
        config=config,
        definition=definition
    )

    numeric_calculator.calculate()

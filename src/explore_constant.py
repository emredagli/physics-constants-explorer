from fractions import Fraction

from tqdm import tqdm

from src.common_library import parse_numeric_value, parse_unit
from src.dimensional_operator import DimensionalOperator
from src.dimensionless_operator import DimensionlessOperator
from src.quantity import Quantity
from src.scope import Scope
from src.validator_library import validate_input, validate_definition, validate_config


class ExploreConstant:
    _SKIP_ON_WHERE_STATEMENT = ["π", "pi"]

    def __init__(self, target_value, target_unit, definition, config):

        validate_input(target_value, target_unit)
        validate_definition(definition)
        validate_config(config, definition)

        self.target = Quantity(
            value=parse_numeric_value(numeric_value=target_value, forced_absolute_error="1"),
            power=Fraction(1),
            unit=parse_unit(target_unit.strip()),
            constant_name="Target",
            symbol="Target")

        self.dimensionless_scope = Scope(
            constants=config.get("dimensionless_constants"),
            definition=definition.get("dimensionless_constants"),
            is_dimensionless=True)

        self.dimensional_scope = Scope(
            constants=config.get("dimensional_constants"),
            definition=definition.get("dimensional_constants"),
            is_dimensionless=False)

        self.dimensionless = DimensionlessOperator(
            scope=self.dimensionless_scope)

        self.dimensional = DimensionalOperator(
            settings=config.get("settings"),
            scope=self.dimensional_scope,
            target=self.target,
            dimensionless_numeric_range=self.dimensionless.numeric_range)

        self.results = None

    def _is_within_the_target_error_range(self, numeric_value, relative_error):
        """Numeric value overlapping check by using relative errors"""
        return 1 - relative_error - self.target.relative_error <= self.target.value / numeric_value <= \
               1 + relative_error + self.target.relative_error

    def explore(self):
        print(f"Explore the target:\n"
              f"\t{self.target.to_string()}\n"
              f"in terms of the given,\n"
              f"\tdimensional constants:   {self.dimensional.scope.get_summary()}\n"
              f"\tdimensionless constants: {self.dimensionless.scope.get_summary()}\n"
              f"by using {self.dimensional.settings.get('method')} methodology...\n")

        results = list()

        self.dimensional.explore_constant()

        self.dimensional.print_the_candidates()

        if len(self.dimensional.candidates_in_range.items()) > 0:
            self.dimensionless.prepare_constants()

            for _, dimensional_quantity in tqdm(self.dimensional.candidates.items(),
                                                desc="Iterating the candidates",
                                                leave=True):
                dimensional_value = dimensional_quantity.value
                for dimensionless_value, dimensionless_quantity in tqdm(
                        self.dimensionless.constants.items(),
                        desc="Iterating the dimensionless constants",
                        leave=False):
                    relative_error = dimensionless_quantity.relative_error + dimensional_quantity.relative_error
                    numeric_value = dimensionless_value * dimensional_value
                    if self._is_within_the_target_error_range(numeric_value=numeric_value,
                                                              relative_error=relative_error):
                        results.append((numeric_value, Quantity(value=[dimensionless_quantity, dimensional_quantity])))

        self.results = results

        # Print the results
        if len(results) > 0:
            print(f"Result(s) that overlap with the target:")
            print(f"\t{self.target.to_string()}")
            for resultant_numeric_value, expression in results:
                print(f"\t{expression.to_string(self.target)}")
            print(f"{self._get_where_statement_of_results()}")
        else:
            print("No results were found that overlapped with the target's numeric value!\n")
            if len(self.dimensional.candidates_in_range.values()) > 0:
                print(f"\t{self.target.to_string()}\n")
                print("But the following candidates were in the given dimensionless range:")
                for candidate in self.dimensional.candidates_in_range.values():
                    print(f"\t{candidate.to_string(self.target)}")

    def _get_where_statement_of_results(self):
        existing_dimensional_constants = set()
        existing_dimensionless_constants = set()
        for _, expression in self.results:
            for term in expression.terms:
                if term.power == 0 or term.symbol in self._SKIP_ON_WHERE_STATEMENT:
                    continue
                if term.is_dimensionless:
                    existing_dimensionless_constants.add(term.constant_name)
                else:
                    existing_dimensional_constants.add(term.constant_name)

        if len(existing_dimensional_constants) + len(existing_dimensionless_constants) == 0:
            return ""

        return f"\nWhere" \
               f"{self.dimensionless_scope.get_where_statement(existing_dimensionless_constants)}" \
               f"{self.dimensional_scope.get_where_statement(existing_dimensional_constants)}"

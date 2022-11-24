from fractions import Fraction

from tqdm import tqdm

from src.dimensional_operator import DimensionalOperator
from src.dimensionless_operator import DimensionlessOperator
from src.quantity import Quantity
from src.scope import Scope
from src.validator_library import validate_input, validate_definition, validate_config


class ExploreConstant:
    def __init__(self, target_value, target_unit, definition, config, unit_registry):
        self.ur = unit_registry

        validate_input(target_value, target_unit, unit_registry)
        validate_definition(definition, unit_registry)
        validate_config(config, definition)

        self.target = Quantity(
            value=target_value,
            power=Fraction(1),
            unit=target_unit.strip(),
            constant_name="Target",
            symbol="Target",
            uncertainty=("0", "10"),
            unit_registry=unit_registry)

        self.dimensionless = DimensionlessOperator(
            scope=Scope(
                constants=config.get("dimensionless_constants"),
                definition=definition.get("dimensionless_constants"),
                allow_missing_definitions=True,
                unit_registry=unit_registry
            ),
            unit_registry=self.ur
        )

        self.dimensional = DimensionalOperator(
            method=config.get("method"),
            scope=Scope(
                constants=config.get("dimensional_constants"),
                definition=definition.get("dimensional_constants"),
                allow_missing_definitions=False,
                unit_registry=unit_registry
            ),
            target=self.target,
            dimensionless_numeric_range=self.dimensionless.numeric_range,
            unit_registry=self.ur
        )

        self.candidates_in_range = None
        self.results = None

    def _is_within_the_target_error_range(self, numeric_value, relative_error):
        """Numeric value overlapping check by using relative errors"""
        return 1 - relative_error - self.target.relative_error <= self.target.value / numeric_value <= 1 + relative_error + self.target.relative_error

    def explore(self):

        print(f"Explore the target quantity:\n"
              f"\t{self.target.to_string()}\n"
              f"in terms of the given:\n"
              f"\tdimensional constants:   {self.dimensional.scope.get_summary()}\n"
              f"\tdimensionless constants: {self.dimensionless.scope.get_summary()}\n"
              f"by using {self.dimensional.method} methodology...\n")

        results = list()

        self.candidates_in_range = []

        self.dimensional.find_matched_multiplications()

        self.dimensional.print_matched_results()

        if len(self.dimensional.matched.items()) > 0:
            self.dimensionless.prepare_dimensionless_constants()

            for dimensional_value, dimensional_quantity in tqdm(self.dimensional.matched.items(),
                                                                desc="Iterating the candidates",
                                                                leave=True):
                if self.dimensionless.is_in_range(self.target.value / dimensional_value):
                    self.candidates_in_range.append(dimensional_quantity)
                    for dimensionless_value, dimensionless_quantity in tqdm(
                            self.dimensionless.constants.items(),
                            desc="Iterating the dimensionless constants",
                            leave=False):
                        relative_error = dimensionless_quantity.relative_error + dimensional_quantity.relative_error
                        value = dimensionless_value * dimensional_value
                        if self._is_within_the_target_error_range(numeric_value=value,
                                                                  relative_error=relative_error):
                            results.append((value, Quantity(
                                value=[dimensionless_quantity, dimensional_quantity],
                                unit_registry=self.ur
                            )))

        self.results = results

        # Display the results
        if len(results) > 0:
            print(f"Result(s) that overlap with the target:")
            print(f"\t{self.target.to_string()}")
            for resultant_numeric_value, expression in results:
                print(f"\t{expression.to_string(self.target)}")
        else:
            print("No results were found that matching with the target!\n")
            if len(self.candidates_in_range) > 0:
                print("But the following candidates were in the given dimensionless range:")
                for candidate in self.candidates_in_range:
                    print(f"\t{candidate.to_string()}")

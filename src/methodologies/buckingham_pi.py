import math
from collections import OrderedDict
from copy import deepcopy
from fractions import Fraction
from itertools import product, combinations

from pint import pi_theorem
from tqdm import tqdm

from src import dimensionless_unit
from src.methodologies.base_methodology import BaseMethodology
from src.quantity import Quantity
from src.scope import Scope


class BuckinghamPI(BaseMethodology):
    _TARGET_NAME = "Target"
    _NAME_SEPERATOR = "__"
    _LIMIT_DENOMINATOR = 1000

    def find_matched(self):
        pi_config_with_target = dict()

        pi_config_with_target[self._get_pi_key(self._TARGET_NAME, Fraction(1))] = self.target.unit

        for constant_name, quantities in self.scope.powered_quantities.items():
            for power, quantity in quantities.items():
                if power == 0:
                    continue
                pi_config_with_target[self._get_pi_key(constant_name, power)] = quantity.unit

        # - WITH Target:
        #         π_1 = ℎ² / (Target⋅e²⋅m_e²⋅µ_0)
        #         π_2 = e² / (Target⋅m_e²⋅ε_0)
        #         π_3 = ℎ⁴ / (Target⁴⋅m_e⁹⋅G_F)
        # - Not found WITHOUT Target!

        # - WITH Target:
        #         π_1 = ℎ² / (e²⋅m_e²⋅µ_0⋅Target)
        # - WITHOUT Target:
        #         π_2 = e⁴⋅µ_0 / (ℎ²⋅ε_0)
        #         π_3 = e⁸⋅µ_0⁴ / (ℎ⁴⋅m_e⋅G_F)

        # Sample Input for "pi_theorem" function:
        #   {'T': '[time]', 'L/T': '[length]/[time]', 'L2': '[length]^2', 'L': '[length]', 'T2': '[time]^2'}
        # and, its output:
        #   [{'T': 2.0, 'L/T': 2.0, 'L2': -1.0}, {'T': 1.0, 'L/T': 1.0, 'L': -1.0}, {'T': -2.0, 'T2': 1.0}]
        # It finds all different powered combinations that the resultant dimension of the multiplication is dimensionless!
        # So, after this calculation we need to find "target" under the result sets and,
        # divide the power of the rest items by target's negative power
        pi_results = pi_theorem(pi_config_with_target)

        pi_results = self._change_power_types_to_fraction(pi_results)
        pi_results = self._filter_duplicate_terms(pi_results)
        pi_results = self._reduce_power_terms(pi_results)
        pi_result_with_target, pi_results_without_target = self._separate_terms_by_target(pi_results)

        if pi_result_with_target is None:
            self.candidates = OrderedDict()
            print(f"Dimensionless π terms could not be found for {self._TARGET_NAME} from the Buckingham π Theorem:")
            return

        pi_results_without_target = self._filter_duplicate_terms(pi_results_without_target)
        pi_results_without_target = self._reduce_power_terms(pi_results_without_target)

        self._print_all_pi_terms(pi_result_with_target, pi_results_without_target)

        buckingham_pi_ranges = Scope.get_power_range(self.settings.get("buckingham_pi_ranges"))

        candidate_terms = []
        if len(pi_results_without_target) > 0:
            pi_products = [buckingham_pi_ranges] * len(pi_results_without_target)
            for pi_product in tqdm(product(*pi_products),
                                   desc=f"Combinations of dimensionless pi terms are being calculated...",
                                   unit=" Iteration",
                                   total=len(buckingham_pi_ranges) * len(pi_results_without_target)):
                candidate_term = self._extract_target_from_pi_term(pi_result_with_target)
                for index, pi_power in enumerate(pi_product):
                    powered_pi_term = self._power_of_term(pi_results_without_target[index], pi_power)
                    candidate_term = self._multiply_terms(candidate_term, powered_pi_term)

                if len(candidate_term) > 0 and self._are_term_powers_in_scope(candidate_term):
                    candidate_terms.append(candidate_term)
        else:
            target_expression = self._extract_target_from_pi_term(pi_result_with_target)
            if self._are_term_powers_in_scope(target_expression):
                candidate_terms.append(target_expression)

        candidate_terms = self._verify_dimensionless_term_is_added(candidate_terms)

        candidates = dict()
        for candidate_term in candidate_terms:
            result_quantities = []
            for constant_name, constant_power in candidate_term.items():
                quantity = deepcopy(self.scope.quantities.get(constant_name))
                quantity.power_of(constant_power)
                result_quantities.append(quantity)
            result_quantity = Quantity(value=result_quantities)
            candidates.setdefault(result_quantity.get_hash(), result_quantity)

        self.candidates = OrderedDict(sorted(candidates.items(), key=lambda item: item[1].value))

    def _reduce_power_terms(self, pi_results: list[dict]) -> list[dict]:
        """
        It reduces the powers of dimensionless pi terms by using:
            the least common multiple for denominators and then
            the greatest common divisor for calculated numerators
        For example, it reduces the power terms of:
            {'Target': Fraction(-12, 1), 'elementary_charge': Fraction(24, 1), 'electron_mass': Fraction(-24, 1), 'vacuum_electric_permittivity': Fraction(-12, 1)}
        To:
            {'Target': Fraction(-1, 1), 'elementary_charge': Fraction(2, 1), 'electron_mass': Fraction(-2, 1), 'vacuum_electric_permittivity': Fraction(-1, 1)}
        """
        result = list()
        for pi_result in pi_results:
            lcm_val = Fraction(math.lcm(*list(map(lambda power: power.denominator, pi_result.values()))))
            reduced_term = {key: val * lcm_val for key, val in pi_result.items()}

            gcd_val = Fraction(math.gcd(*list(map(lambda power: power.numerator, reduced_term.values()))))
            result.append({key: val / gcd_val for key, val in reduced_term.items()})
        return result

    def _filter_single_constant_terms(self, pi_results: list[dict]) -> list[dict]:
        """
        It removes pi results which contains a single constant expect Target.
        For example the following pi result needed to be removed:
            {'elementary_charge__-4': -1.0, 'elementary_charge__-1': 4.0}
        """
        result = list()
        for pi_result in pi_results:
            constant_names = set()
            for pi_key, constant_power in pi_result.items():
                constant_name, _ = self._get_powered_constant_from_pi_key(pi_key)
                constant_names.add(constant_name)

            if len(constant_names) != 1 or self._TARGET_NAME in constant_names:
                result.append(pi_result)
        return result

    def _change_power_types_to_fraction(self, pi_terms: list[dict]) -> list[dict]:
        """
        It converts pi term item's powers to actual values. Such that, it converts the following pi term,
            {'Target__1': -12.0, 'elementary_charge__-4': -6.0, 'electron_mass__-3': 8.0, 'vacuum_electric_permittivity__-4': 3.0}
        to:
            {'Target': -12.0, 'elementary_charge': 24.0, 'electron_mass': -24.0, 'vacuum_electric_permittivity': -12.0}

        On multiplication, it also converts power types to Fraction
        """
        results = list()
        for pi_term in pi_terms:
            result = dict()
            for pi_key, pi_power in pi_term.items():
                if pi_power != 0:
                    constant_name, constant_power = self._get_powered_constant_from_pi_key(pi_key)
                    result[constant_name] = result.get(constant_name, Fraction(0)) + \
                                            (Fraction(constant_power) * Fraction(pi_power)).limit_denominator(
                                                self._LIMIT_DENOMINATOR)

            cleaned_result = self._clean_zero_powers(result)

            # Filter terms which has no constants
            if len(cleaned_result) > 0:
                results.append(cleaned_result)
        return results

    def _get_pi_key(self, constant_name, power):
        return constant_name + self._NAME_SEPERATOR + str(power)

    def _get_powered_constant_from_pi_key(self, pi_key):
        constant_name, power_str = pi_key.split(self._NAME_SEPERATOR)
        return constant_name, power_str

    def _get_first_pair(self, iterable):
        return next(iter(iterable.items()))

    def _print_all_pi_terms(self, pi_result_with_target: dict, pi_results_without_target: list[dict]):
        print(f"Dimensionless π terms found from the Buckingham π Theorem:")
        index = self._print_pi_terms([pi_result_with_target], include_target=True)
        self._print_pi_terms(pi_results_without_target, include_target=False, last_index=index)
        print("")

    def _print_pi_terms(self, pi_results: list[dict], include_target: bool, last_index=0) -> int:
        if len(pi_results) == 0:
            return last_index

        explanation = f"Containing {self._TARGET_NAME}" if include_target else f"Not containing {self._TARGET_NAME}"
        print(f"- {explanation}:")

        index = 0
        for index, pi_theorem_result in enumerate(pi_results):
            quantities = []
            for constant_name, power in pi_theorem_result.items():
                if constant_name == self._TARGET_NAME:
                    reference_quantity = self.target
                else:
                    reference_quantity = self.scope.quantities.get(constant_name)

                quantity = deepcopy(reference_quantity)
                quantity.power_of(power)
                quantities.append(quantity)

            print(f"\tπ_{index + last_index + 1} = {Quantity(value=quantities).get_expression_with_solidus()}")
        return index + 1

    def _separate_terms_by_target(self, pi_results_with_target: list[dict]) -> (dict, list[dict]):
        with_target = list()
        without_target = list()
        for pi_term in pi_results_with_target:
            if self._TARGET_NAME in pi_term:
                with_target.append(pi_term)
            else:
                without_target.append(pi_term)

        if len(with_target) > 1:
            target_term, derived_dimensionless_terms = self._get_dimensionless_terms_from_target_terms(with_target)
            without_target = without_target + derived_dimensionless_terms
        elif len(with_target) == 1:
            target_term = with_target[0]
        else:
            target_term = None

        return target_term, without_target

    def _get_dimensionless_terms_from_target_terms(self, with_target: list[dict]) -> (dict, list[dict]):
        """
        It traverses combination of 2 unique tuples from pi terms, such that:
            π_1, π_2, ..., π_n
            (π_1, π_2), (π_1, π_3), ...
        and for each (π_i, π_j):
            1. Extract Target from dimensionless pi terms
            2. Divide terms to derive a new dimensionless pi term

        The main reason here, we would like to apply all dimensionless pi combinations to a single Target term.
        So all the rest can be treated as dimensionless. Duplicate dimensionless pi terms will be filtered.

        :param with_target: list of pi terms that contain Target
        :return: a tuple of (first item of with_target, derived dimensionless terms)
        """
        target_term = with_target[0]
        derived_dimensionless_terms = list()
        for term_1, term_2 in combinations(with_target, 2):
            term_1_in_target = self._extract_target_from_pi_term(term_1)
            term_2_in_target = self._extract_target_from_pi_term(term_2)
            derived_dimensionless_terms.append(self._multiply_terms(term_1_in_target,
                                                                    self._power_of_term(
                                                                        term_2_in_target,
                                                                        Fraction(-1))))

        return target_term, derived_dimensionless_terms

    def _are_term_powers_in_scope(self, term: dict) -> bool:
        for constant_name, constant_power in term.items():
            matched_quantity = self.scope.powered_quantities.get(constant_name, dict()).get(Fraction(constant_power))
            if matched_quantity is None:
                return False
        return True

    def _multiply_terms(self, term_1: dict, term_2: dict) -> dict:
        """
        It multiplies 2 pi terms and removes zero powered constants
        :param term_1:
        :param term_2:
        :return:
        """
        result = deepcopy(term_1)
        for constant_name, constant_power in term_2.items():
            # TODO verify .limit_denominator() needing
            result[constant_name] = (constant_power + result.get(constant_name, Fraction(0))).limit_denominator(
                self._LIMIT_DENOMINATOR)

        cleaned_result = self._clean_zero_powers(result)

        return cleaned_result

    def _clean_zero_powers(self, pi_term):
        # Clean zero powered constants from result
        result = dict()
        for constant_name, constant_power in pi_term.items():
            if constant_power != 0:
                result[constant_name] = constant_power
        return result

    def _power_of_term(self, pi_term_without_target: dict, power: Fraction) -> dict:
        result = dict()
        for constant_name, constant_power in pi_term_without_target.items():
            # TODO verify .limit_denominator() needing
            result[constant_name] = (constant_power * power).limit_denominator(self._LIMIT_DENOMINATOR)
        return result

    def _extract_target_from_pi_term(self, pi_term_with_target: dict) -> dict:
        result = dict()
        target_power = pi_term_with_target.get(self._TARGET_NAME)
        for constant_name, power in pi_term_with_target.items():
            if constant_name == self._TARGET_NAME:
                continue
            # TODO verify .limit_denominator() needing
            result[constant_name] = (-1 * power / target_power).limit_denominator(self._LIMIT_DENOMINATOR)
        return result

    def _filter_duplicate_terms(self, pi_terms: list[dict]) -> list[dict]:
        """
        It filters same dimensionless pi terms such that:
            π_i = (π_j) ^ R
            R ∈ Real Numbers
        To achieve this:
            1. Sort constants by its name
            2. Take first item power as reference "ref_power"
            3. Calculate the power of each item by dividing to "ref_power"
            4. Create a unique key by using powers calculated on previous step
            5. Filter pi terms if it has the same key
        """
        result = list()
        keys = set()
        for pi_term in pi_terms:
            constants = list(pi_term.keys())
            constants.sort()
            ref_power = pi_term.get(constants[0])
            key = "-".join([f"{c}_{(pi_term[c] / ref_power)}" for c in constants])
            if key not in keys:
                keys.add(key)
                result.append(pi_term)
        return result

    def _verify_dimensionless_term_is_added(self, pi_terms: list[dict]) -> list[dict]:
        if self.target.unit.units != dimensionless_unit.units:
            return pi_terms

        contains_empty_term = False
        for pi_term in pi_terms:
            if len(pi_term) == 0:
                contains_empty_term = True
                break

        if contains_empty_term:
            return pi_terms
        else:
            return pi_terms + [{}]

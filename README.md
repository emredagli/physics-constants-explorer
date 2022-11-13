# Physics Constants Explorer

This work contains research and a python program to explore physical constants formulation in terms of given other physical and mathematical constants.

## Table of Content

<!-- TOC -->
* [Motivation & Concept](#motivation--concept)
* [Methodology](#methodology)
* [Python Installation](#python-installation)
* [Running the Program](#running-the-program)
  * [Constants Definition File](#constants-definition-file)
  * [The Config File](#the-config-file)
  * [The Program Inputs](#the-program-inputs)
* [The Program Outputs](#the-program-outputs)
  * [Store Results into a File](#store-results-into-a-file)
  * [Output Format](#output-format)
    * [Summarizing the Inputs](#summarizing-the-inputs)
    * [Listing the Candidates](#listing-the-candidates)
    * [Matched Results](#matched-results)
* [Tests](#tests)
* [Researches](#researches)
* [Resources](#resources)
  * [Libraries & Documentation](#libraries--documentation)
* [Future Work](#future-work)
* [Decided TODO list:](#decided-todo-list-)
* [Gratitude](#gratitude)
<!-- TOC -->

## Motivation & Concept

Most of the relations in physics are observed from experiments and constants in the relations measured by instruments within the given error range.

For example Stefan-Boltzmann Constant, [Josef Stefan](https://en.wikipedia.org/wiki/Josef_Stefan) had found the relation between radiation power and temperature of the black body radiation problem:

```math
j^{\star} = \sigma T^{4}
```

where,

* $j^{\star}$ is radiated power per unit area
* $T^{4}$ is 4. power of radiated material's temperature
* $\sigma$ is a __physical constant__ (known as Stefan–Boltzmann constant)

Theoretical formulation of $\sigma$ was done by [Ludwig Eduard Boltzmann](https://en.wikipedia.org/wiki/Ludwig_Boltzmann):

```math
\sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}} \approxeq 5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}
```

where

* $k$ is the [Boltzmann constant](https://en.wikipedia.org/wiki/Boltzmann_constant) (another physical constant)
* $h$ is the [Planck constant](https://en.wikipedia.org/wiki/Planck_constant) (another physical constant)
* $c$ is the [Speed of Light](https://en.wikipedia.org/wiki/Speed_of_light) in vacuum (physical constant)
* $\pi$ is the ratio of a circle's circumference to its diameter (mathematical constant)

with SI base units:

* kg is kilogram
* s is second
* K is Kelvin

Formulation of $\sigma$ was [theoretically derived](https://edisciplinas.usp.br/pluginfile.php/48089/course/section/16461/qsp_chapter10-plank.pdf) by using the other physical and mathematical constants.

Now, let's think oppositely and assume we have a function which takes:

* Target value: 5.670374419E-8 (in [Scientific Notation](https://en.wikipedia.org/wiki/Scientific_notation))
* Target unit: $\mathrm{kg}\\times\mathrm{s}^{-3}\\times\mathrm{K}^{-4}$
* List of physical constants with their units ( $k$, $h$, $c$, ...)
* List of mathematical constants ( $\pi$, $e$, ...)
* List of prime numbers (2, 3, 5, ...)

and returns the matched formula(s), so that:

* The target unit is "exactly" matched with the unit of formula and,
* The target value is matched with the resultant numeric value (within the given error range).

Example Output:

```text
(5.6703744195 ± 0.0000000005)✕10⁻⁸ kg/K⁴/s³  ≈  2 ⋅ pi⁵ ⋅ boltzmann_constant⁴ / (3 ⋅ 5 ⋅ speed_of_light² ⋅ planck_constant³)
```

Would it be possible and useful?

Yes it is possible. To be honest, I am not definitely sure about its usefulness!

But I would like to start this study with the excitement of opportunity of being the first person to see the possible formulation of some famous physical constants.
And I know that this methodology can be expanded to a wider scope with distributed calculation methods if this PoC can be successful.

## Methodology

It is a well-known fact that the resultant physical unit on the right side of the equations must match the left side.

This is the main methodology that I have followed:

1. Preparing the candidate list by calculating the combination of physical constants which matched the target unit.
2. Iterating over the candidates, looking for a combination of dimensionless mathematical constants, such that the resulting multiplication places within the desired error range.

![Flowchart of Physical Constants Explorer](./img/Flowchart_of_Physical_Constants_Explorer.drawio.svg)

I wanted to apply a simple and clear set of methodologies:

1. Brute force algorithm for all multiplication combinations
2. Using a unit library ([pint](https://pint.readthedocs.io/en/stable/)) to:
   * Represent physical dimensional constants
   * Convert physical constants and multiplications to base SI units
   * Correctly calculate the multiplication of physical and mathematical constants
3. Using scientific notation with the ["concise form"](https://en.wikipedia.org/wiki/Scientific_notation#Estimated_final_digits) for input target values.
4. Ignore errors on the right side of the equation (with assuming the left-hand side of the equation is the target), i.e. resultant error of the combination of the calculated multiplications.
5. Using [decimal](https://docs.python.org/3/library/decimal.html) library to represent numbers with high significant digits (50 is set as default precision)
6. Using the same config file on exploring well-known physical constants section. With this methodology we may have a base config that can help us to explore unknown constants.

## Python Installation

The implementation is done by using Python 3.9.13

If python is not installed, I suggest using one of "Python Version Manager" (Anaconda, pyenv, etc.)

Please execute the following code, line by line on the projects root folder:

```shell
> python -m venv ./venv
> source ./venv/bin/activate
> python -m pip install --upgrade pip
> pip install -r ./requirements.txt
```

## Running the Program

### Constants Definition File

The program is using [pint](https://pint.readthedocs.io/en/stable/) library to use and operate on physical (dimensional) & mathematical (dimensionless) constants.

TODO: Add another parameter...
You can override to modify [pint default constants definition file](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt).

### The Config File

TODO: move default config to the root or under the src.
The config file is required to restrict the program scope. The default [config/config.json](config/config.json)) file and its format:

```json
{
  "physical_constants": {
    "method": "brute_force",
    "constants_and_powers": {
      "speed_of_light": [-4, 4],
       ...
    }
  },
  "mathematical_constants": {
    "numbers_and_powers": {
      "2": [-5, 5],
      ...
    },
    "constants_and_powers": {
      "pi": [-5, 5],
      ...
    }
  }
}
```

The file holds the constants and their power ranges that the program will consider & calculate.


| Root Setting                                                          | Sub Setting            | Keys                                                                                                                      | Values                                                                                                                                                                                                                             |
| --------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "physical_constants"                                                  | "method"               |                                                                                                                           | "brute_force"                                                                                                                                                                                                                      |
| "physical_constants"                                                  | "constants_and_powers" | Dimensional physical constant name. It must be defined on[the definition file](research/definition/constants_en.txt).            | The power range.<br/>* `Array`: `[min, max]`. The program converts it as integer range e.g. `[min, ..., max]`. It adds `0`, if `0` does not exist in the range.<br/>* `Integer`: the program converts it as `[-value, ..., value]` |
| "mathematical_constants"                                              | "numbers_and_powers"   | Prime numbers in string format e.g. "2"                                                                                   | The power range. The format is the same as above.                                                                                                                                                                                  |
| "mathematical_constants"                                              | "constants_and_powers" | Dimensionless mathematical constant name. It must be defined on[the same definition file](research/definition/constants_en.txt). | The power range. The format is the same as above.                                                                                                                                                                                  |
| The result of the calculation is represented in terms of`key` values. |                        |                                                                                                                           |                                                                                                                                                                                                                                    |

### The Program Inputs

The program `main.py` takes target value and unit with the following input names:

* `--target-value`
* `--target-unit`
* `--config-path` (optional)

As an example, to explore `Rydberg Constant`:

```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m"
```

Please use `--help` option to get more info about the program usage:

```shell
> python ./main.py --help

options:
  -h, --help            show this help message and exit
  -v, --target-value 
                        Target value with scientific notation.
                        To specify target value with the standard uncertainty please use "concise form".
                        For example to provide this value (1.23±0.06)×10^−5, enter "1.23(6)E-5".
                        Some examples: "1.23(6)E-5", "8.9875(15)E+16", "4.2(3)E+0"
                        The target value can also be provided without uncertainty specification:
                        In this cae, the program converts "1.23E-5" to "1.235(5)E-5"
                        Some examples: "1.23E-5", "8.9875E+16", "4.2E+0"
  -u, --target-unit 
                        Target unit expression in terms of SI base units symbols.
                        Length - meter (m)
                        Time - second (s)
                        Amount of substance - mole (mol)
                        Electric current - ampere (A)
                        Temperature - kelvin (K)
                        Luminous intensity - candela (cd)
                        Mass - kilogram (kg)
                        Please use ^ symbol to represent power and space for multiplication.
                        Some examples: "kg/(s^3 K^4)", "kg s^-3 K^-4", "m/s"
  -c, --config-file 
                        The config file relative path.
                        It is a JSON file that contains the list of physical and mathematical constants
                        with their power ranges. This file is validated by "src/resources/config_schema.json"
                        If it is not provided the program will use default config file:
                        ./src/resources/default_config.json
  -d, --definition-file 
                        Definition file relative path.
                        If it is not provided the program use pint library default definition file:
                        https://github.com/hgrecco/pint/blob/master/pint/default_en.txt
                        And loads default physical constant definitions:
                        https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt
                        To customize it, please copy these 2 files, make customization on constants_en.txt file
                        and reference default_en.txt relative path for this parameter.
                        Please look at the examples given on the Readme.md file
```
## The Program Outputs

The program prints the outputs to console. 

### Store Results into a File

You can store the results into a file by executing the script like:

```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m" > output_file_name.txt
```
It will store the results into `output_file_name.txt` file on the same folder that you execute the script.

### Output Format

There are 3 sections on the output. The following part explains the sections of the `Rydberg Constant` exploration:

#### Summarizing the Inputs
```text
Search the target:
	(1.0973731568160 ± 0.0000000000021)✕10⁷ 1/m
in terms of the given:
	physical constants:     
		speed_of_light ^ [-2, -1, 0, 1, 2]
		planck_constant ^ [-3, -2, -1, 0, 1, 2, 3]
		boltzmann_constant ^ [-4, -3, -2, -1, 0, 1, 2, 3, 4]
		elementary_charge ^ [-4, -3, -2, -1, 0, 1, 2, 3, 4]
		electric_constant ^ [-2, -1, 0, 1, 2]
		electron_mass ^ [-1, 0, 1]
		avogadro_constant ^ [-1, 0, 1]
	mathematical constants: 
		pi ^ [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
		wien_u ^ [-1, 0, 1]
		2 ^ [-3, -2, -1, 0, 1, 2, 3]
		3 ^ [-1, 0, 1]
		5 ^ [-1, 0, 1]
by using brute_force methodology...
```

#### Listing the Candidates
After checking all combination of the physical constants given in the scope, the program prepares the candidates list whose resultant unit matches the target unit.

All mathematical multiplication combinations are calculated if there is at least one candidate in the result.

```text
Totally, unique 2079 mathematical multiplications are calculated & cached!
Found 4 candidates the resultant unit matched with the target's unit:
	[ M ] [ 1/m ] = elementary_charge⁴ ⋅ electron_mass / (speed_of_light ⋅ planck_constant³ ⋅ electric_constant²)
	  ├── 👍 In range!
	  └──  Min (~1✕10²) < M̲ ̲(̲~̲9̲✕̲1̲0̲⁷̲)̲ < Max (~1✕10¹²) 

	[ M ] [ 1/m ] = elementary_charge² ⋅ electron_mass / (planck_constant² ⋅ electric_constant)
	  ├── 👍 In range!
	  └──  Min (~1✕10²) < M̲ ̲(̲~̲6̲✕̲1̲0̲⁹̲)̲ < Max (~1✕10¹²) 

	[ M ] [ 1/m ] = speed_of_light ⋅ electron_mass / planck_constant
	  ├── 👍 In range!
	  └──  Min (~1✕10²) < M̲ ̲(̲~̲4̲✕̲1̲0̲¹̲¹̲)̲ < Max (~1✕10¹²) 

	[ M ] [ 1/m ] = speed_of_light² ⋅ electric_constant ⋅ electron_mass / elementary_charge²
	  ├── 👎 Not in range.
	  └──  Min (~1✕10²) < Max (~1✕10¹²) < M̲ ̲(̲~̲3̲✕̲1̲0̲¹̲³̲)̲ 
```
About the first line, if you multiply the length of mathematical constants powers:

`2079 = 11 x 3 x 7 x 3 x 3` combination count can be verified.

If you look at the first candidate:
```text
...
	[ M ] [ 1/m ] = elementary_charge⁴ ⋅ electron_mass / (speed_of_light ⋅ planck_constant³ ⋅ electric_constant²)
	  ├── 👍 In range!
	  └──  Min (~1✕10²) < M̲ ̲(̲~̲9̲✕̲1̲0̲⁷̲)̲ < Max (~1✕10¹²) 
...
```
The program calculated physical constants multiplication and represented its numerical value as `[ M ]` and its unit as `[ 1/m ]`.

`Min` and `Max` values are calculated as:

`Min (...)` = [Target value] / [The maximum value of the mathematical multiplication combinations]

`Max (...)` = [Target value] / [The minimum value of the mathematical multiplication combinations]

So, the line represents:

`	  └──  Min (~1✕10²) < M̲ ̲(̲~̲9̲✕̲1̲0̲⁷̲)̲ < Max (~1✕10¹²) `:

`M` is in the range of mathematical multiplication range. If it is not in range, this candidate is ignored and its numerical value match is not investigated on the next steps.

This distinction is highlighted as `👍 In range!` or `👎 Not in range.`.

#### Matched Results
At the end, the program lists numerically matched results (which rely on the target error range) from the candidate list:

```text
Result(s) matched the target:
	(1.0973731568160 ± 0.0000000000021)✕10⁷ 1/m
	 1.0973731568160✕10⁷ 1/m ≈ elementary_charge⁴ ⋅ electron_mass / (2³ ⋅ speed_of_light ⋅ planck_constant³ ⋅ electric_constant²)
```

## Tests

Test folder is [src/tests](src/tests). To run the all test:

```shell
> pytest
```

## Researches

Some well-known physical constant values were searched and verified by using this program.

Unknown physical constants like Newtonian Constant of Gravitation (G) are also researched under the same [./research](./research) folder.

## Resources

### Libraries & Documentation

* [pint](https://pint.readthedocs.io/en/stable/)
  * [pint repository](https://github.com/hgrecco/pint/tree/master/pint)
  * [pint default constants definition file](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt)
  * [pint developer reference](https://pint.readthedocs.io/en/stable/developers_reference.html)
  * [pint tutorıal](https://pint.readthedocs.io/en/stable/tutorial.html)
* [decimal](https://docs.python.org/3/library/decimal.html)
* [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/) is used to validate the config file.
* [Latex Mathematics](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
  * [Writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)

TODO: check Resources section under the reasearch part. It should include the remove part below.

## Future Work

* For found results, display the previous and next mathematical values to understand how accurately the numerical values to the right of the equation fall within the target error range.
* Investigate possibility of finding all (known) physical constants with a single config file? Targeting `1.0000` with `dimensionless` methodology can be usefully for this purpose, like:

```shell
> python ./main.py --target-value "1.00000E+0" --target-unit ""
```

* Calculate total error value on physical constants multiplications and show it on the result. It will be the error of the right side of the equation. To achieve that, define error values in the definition file. Pint library may also have some features for this purpose. Or [uncertainties library](https://uncertainties-python-package.readthedocs.io/en/latest/) can be a good candidate!
* Implement Cache & [check optimization suggestions of pint](https://pint.readthedocs.io/en/stable/advanced/performance.html)
* Store results into the output file. Currently, results are printed to the console.
* Use python [logging](https://docs.python.org/3/howto/logging.html) instead of `print` after implementing the output file.

## Decided TODO list:
* Reformat config as:
  * dimensional_constants
  * dimensionless_constants
  * Reason, mathematical & physical is not a good separation of concepts. For example fine structure constant, it is a physical dimensionless constants!
* Show results in formatted:
  * pint-formatter: https://pint.readthedocs.io/en/stable/api/specific.html#pint-formatter
  * pint-formatter code: https://github.com/hgrecco/pint/blob/ef0c51944264f2917bf50fb1743bd3f6a214e6fb/pint/formatting.py#L57
  * Or implement your own
* Reformat config file to:
  * To show results with errors.
    * Check how to use pint-formatter with this.

## Gratitude

I would like to express my gratitude to my physics teachers:

* Physics Teacher Rafet Kamer, Physics Olympiads
* Prof. Dr. K. Sinan Bilikmen, METU-Physics
* Prof. Dr. Mehmet Tomak, METU-Physics

And who are not with us:

* Prof. Dr. İbrahim Günal (R.I.P), METU-Physics
* Prof. Dr. Ordal Demokan (R.I.P), METU-Physics
* Physics Teacher Aykut Gümüç (R.I.P), Eskisehir Science High School
* Prof. Dr. Oleg Fedorovich Kabardin (R.I.P), Physics Olympiads

And special thanks to my genius and big-hearted friends who always enjoy supporting me:

* Dr. İnanç Kanık
* Dr. Özgür Sümer
* Atılım Çetin
* Osman Özgür
* Ali Onur Geven

And to my beloved wife Ayşen and my dear children Ozan & Doruk!

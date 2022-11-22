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
* $T^{4}$ is 4th power of radiated material's temperature
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
{ 5.6703744191844... e-8 (exact) } [ kg/K⁴/s³ ] = 2⋅π⁵⋅k⁴ / (3⋅5⋅c²⋅ℎ³)
```

Would it be possible and useful?

Yes it is possible. To be honest, I am not definitely sure about its usefulness!

But I would like to start this study with the excitement of opportunity of being the first person to see the possible formulation of some famous physical constants.
And I know that this methodology can be expanded to a wider scope with distributed calculation methods if this approach can be successful and be considered as useful.

## Methodology

It is a well-known fact that the resultant unit on the right side of the equations must match the left side.

```text
Quantity = {numeric value} ⋅ [unit]

Q1 = {Q1} ⋅ [Q1]
Q2 = {Q2} ⋅ [Q2]

If Q1 = Q2 then units must be equal, [Q1] = [Q2].
```
If we claim Q1 = Q2 then their numeric values should also overlap in their error ranges:
```text
Quantity = {numeric value ± error} ⋅ [unit]

Q1 = {Q1 ± ΔQ1}⋅[Q1]
Q2 = {Q2 ± ΔQ2}⋅[Q2]

To claim Q1 = Q2:
* [Q1] = [Q2], and
* {Q1 + ΔQ1} >= {Q2 - ΔQ2}, and
* {Q1 - ΔQ1} <= {Q2 + ΔQ2}
```

In the program, we can assume `Q1` is the target (`T`) and it is searching set of `Q2`'s which are the candidates satisfying the conditions given above.

The program also takes config ([default](src/resources/default_config.json)) and definition ([default](src/resources/default_definition.json)) files to restrict and define its scope.

The main steps can be summarized as:

1. Preparing the candidate list by calculating the combination of dimensional constants from the given scope such that unit of `T` equals to unit of the candidates (e.g. `[T] = [Q]`)
2. Iterating over the candidates, looking for a combination of dimensionless mathematical constants, such that the resulting multiplication places within the desired error range.
3. Printing the results by using their symbols.

![Flowchart of Physical Constants Explorer](./img/Flowchart_of_Physical_Constants_Explorer.drawio.svg)

I wanted to apply a simple and clear set of methodologies:

1. Brute force algorithm for all multiplication combinations
2. Using a unit library ([pint](https://pint.readthedocs.io/en/stable/)) to:
   * Represent dimensional constants units in SI base units
   * Correctly calculate and compare the units of multiplication and power operations
3. Using scientific notation with the ["concise form"](https://en.wikipedia.org/wiki/Scientific_notation#Estimated_final_digits).
4. Calculating the relative errors.
5. Using [decimal](https://docs.python.org/3/library/decimal.html) library to represent numeric values of quantities with high significant digits.
6. Using [fractions](https://docs.python.org/3/library/fractions.html) library to represent the power of the quantities and its units.

### Technical Reasons

* Python's Decimal library was used to calculate the mathematical operations of the numeric values of the quantities.
* The "pint" library in conjunction with the Python's Fractions library was used to calculate the mathematical operations of the units part of the quantities.

The main reasons about this technical decisions are:
1. Python Fractions library we can make this kind of rational mathematical operations correctly: [$s^{2/3}$] ⋅ [$s^{4/3}$] ≟ [$s^{2}$]
2. "pint" library has support for "Non integer types" (non_int_type) to set `Decimal` or `Fractions`. But, unfortunately I could not find a feature to set numeric and unit parts class types differently.  
3. Decimal Library has nice set of features to represent high precision numbers and operate on it quickly.
4. It is not wanted to use another library to handle the measurement error calculations of the numeric values. The main reason is to add less complexity. Only Python's built-in Libraries are used. So it can be implemented more robustly and more testable.

Please do not hesitate to provide feedback if you have suggestions, thanks!

## Python Installation

The implementation is done by using Python 3.9.13. The program should run Python >=3.9.13

If python is not installed, I suggest using one of "Python Version Manager" (Anaconda, pyenv, etc.)

Please execute the following code, line by line on the projects root folder after cloning this repository.

```shell
> python -m venv ./venv
> source ./venv/bin/activate
> python -m pip install --upgrade pip
> pip install -r ./requirements.txt
```

## Running the Program

The program takes:
* The target quantity numeric value (mandatory)
* The target quantity unit (mandatory)
* The definition file (optional), that is a list of all dimensional and dimensionless constant definitions as a JSON file.
* The config file (optional), that is the scope of the program. It is a list of dimensional and dimensionless constants and their power ranges as a JSON file.

The program prints the results in descriptive format on the console.

### The Definition File

All dimensional and dimensionless constants are defined under this JSON file. The program loads and considers only the constants selected from here.

The program uses its [default definition file](src/resources/default_definition.json), if `--definition-file` parameter is not provided.
The default definition file is prepared by using [CODATA](https://physics.nist.gov/cuu/Constants/index.html) values which are the latest experimented and defined values.
If you want to add new constants or override the existing ones, please check [The Program Inputs](#the-program-inputs) section to get more info.

To make the numeric values be consistent, only SI base units are allowed as units of dimensional constants.

The definition file has 2 main collections:
* `dimensional_constants`
* `dimensionless_constants`

Each collection has its own `key`, `value` pairs, for example:
```json
{
  "dimensional_constants": {
    "speed_of_light_in_vacuum": {
      "numeric_value": "2.99792458e+8",
      "unit": "m/s",
      "symbol": "c"
    },
    ...
  },
  "dimensionless_constants": {
    "pi": {
      "numeric_value": "3.1415926535897932384626433832795028841971693993751",
      "symbol": "π"
    },
    ...
  }
}
```
#### Dimensional Constants Collection

This collection should only contain constants that have units.

It has the following key-value pair definitions:
* `key` values should contain a descriptive info (on the given example above it is `speed_of_light_in_vacuum`).
* `value` object has the following kay-value pairs:
  * `"numeric_value": "..."` (mandatory). 
    * The values should be in scientific notation format.
    * `"2.99792458e+8"`, if it is an exact value. The error will be 0 for the constants in this format.
    * `"6.67430(15)e-11"`, if it has some error. The format is a combination of both scientific and concise notations. The program considers this value as `(6.67430 ± 0.00015)✕10⁻¹¹`
  * `"unit": "..."` (mandatory). 
    * Only SI base units are accepted: m, s, mol, A, K, cd, kg
    * The following characters can be used:
      * a single space for multiplication
      * `/` for divisions
      * `^` for powers
      * `(...)` parentheses for grouping
    * The following examples which gives the same resultant unit for "Vacuum magnetic permittivity constant" :
      * `A^2 s^4/kg/m^3` = `A^2 s^4/(kg m^3)` = `A^2 s^4 kg^-1 m^-3` 
  * `"symbol": "..."` (optional). 
    * The symbol is used on the results. If it is not provided the `key` value is used on the required places.
  * `"info": "..."` (optional). 
    * If it is needed, this field can be used to enter more information.

#### Dimensionless Constants Collection

This collection should only contain constants that have no units.

It has the same key-value pairs with the same formats as the "Dimensional Constants Collection" except for `unit` definitions. It should not contain the `unit` definitions.

### The Config File

The configuration file determines which constants the program will use to find results close to the desired target value.

Within this file, the list of dimensional and dimensionless constants is defined along with their power ranges.
In this file, a list of dimensional and dimensionless constants is entered along with their power ranges.

The program uses its [default config file](src/resources/default_config.json), if `--config-file` parameter is not provided. [The Program Inputs](#the-program-inputs) section gives the info about the usage of `--config-file` parameter.

The default config file is prepared by exploring some derived physical constants. You can check the list of these derived constants under [the research document](/research).

The config file has the following parameters:
* `method`
* `dimensional_constants`
* `dimensionless_constants`

Each `constant` collection has its own `key`, `value` pairs, for example:
```json
{
  "method": "brute_force",
  "dimensional_constants": {
    "speed_of_light_in_vacuum": [-2, 6],
    "vacuum_magnetic_permeability": {"range": [0, 2], "step": "1/3"},
    ...
  },
  "dimensionless_constants": {
    "pi": 4,
    ...
  }
}
```

The `key` values (for example `speed_of_light_in_vacuum`) should match the `key` values on the provided definition file. 
Besides this, you can also provide exact custom numeric values (such as prime numbers) under `dimensionless_constants` collection without defining it under the definition file. For example:
```json
{
  ...
  "dimensionless_constants": {
    "2": 8,
    ...
  }
```

Power range values can be in 3 format as given the example above:
* List format (`[min, max]`)
  * For example `[-2, 6]`, the program converts it as integer range e.g.[-2, 1, 0, 1, 2, 3, 4, 5, 6]. It adds `0`, if `0` does not exist in the range.
* Integer format (Z). Z>0
  * The program converts it as list format `[-Z, Z]` as explained above.
* Object format (`{"range": [min, max], "step": "s"}`)
  * For the given example above, program creates the powers ranges as, [0, 1/3, 2/3, 1, 4/3, 5/3, 2]


### The Program Inputs

The program `main.py` takes target value and unit with the following input names:

* `--target-value`
* `--target-unit`
* `--config-file` (optional)
* `--definition-file` (optional)

As an example, to explore `Rydberg Constant`:

```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m"
```

Please use `--help` option to get info about the program usage & input formats:

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
* [Python fractions](https://docs.python.org/3/library/fractions.html)
  * It is used on the mathematical operations of the unit part of the quantities
* [Python decimal](https://docs.python.org/3/library/decimal.html)
  * It is used on the mathematical operations of the numeric value of the quantities
* [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/) 
  * It is used to validate the JSON files.
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
  * Mathematical operators and symbols in Unicode: https://en.wikipedia.org/wiki/Mathematical_operators_and_symbols_in_Unicode
  * Or implement your own
* Reformat config file to:
  * To show results with errors.
    * Check how to use pint-formatter with this.
* It has very important information related with the research: https://en.wikipedia.org/wiki/Physical_constant#Number_of_fundamental_constants


## About Me and History of the Program

I am a computer engineer with a background in Scientific Computing and Physics. 
Last 4 years I am mainly working in big data related subjects and domains.  

When I was in high school, I was selected to the Physics Olympic team of my home country. I was 2. on our team and won the honourable mention award in [IPhO 1996 (XXVII Oslo, Norway)](https://www.ipho-new.org/documentations/#statistics).

In the same year, I won the Computer Engineering department in my country's university exam and I decided to study computer engineering due to the conditions of the country I live in.

When I look back now, I was very happy to see that my physics knowledge was still not erased and that I could remember some of them with a short effort.

To admit, we talked about the feasibility of this program 20 years ago, in a conversation with my close friend Atilim Cetin. 
In those years, I did not attempt to implement this program because I had just graduated and my priorities were different.
And frankly, if there weren't libraries like the [pint](https://pint.readthedocs.io/en/stable/) quantity library which helps to dealing with units parts of the quantities, 
I might not have enough energy to get into this. I would like to thank all the team who have developed the pint library from here.

I don't know if a similar physical constant explorer program has been done before. 
If it has been done already, I hope this approach gives a new perspective on helping us to understand the mystery of nature with good purposes!

[Emre Dagli - Linkedin](https://www.linkedin.com/in/emre-dagli/) 

## Gratitude

I would like to express my gratitude to my physics teachers who made me love physics and prepared us for the physics olympiads:

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

And to my parents Muazzez Dagli & Sadi Dagli who are retired math teacher!
And to my beloved wife Ayşen and my dear children Ozan & Doruk!

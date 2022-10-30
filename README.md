# Physics Constants Explorer

This work contains research and a python program to explore physical constants formulation in terms of given other physical & mathematical constants.

<!-- TOC -->
* [Motivation & Concept](#motivation--concept)
* [Methodology](#methodology)
* [Python Install](#python-install)
* [Running the Program](#run-the-program)
  * [Constants Definition File](#constants-definition-file)
  * [The Config File](#the-config-file)
  * [The Program Inputs](#the-program-inputs)
* [Exploring Well-known Physical Constants](#exploring-well-known-physical-constants)
  * [Stefan Boltzmann Constant](#stefan-boltzmann-constant)
  * [Rydberg Constant](#rydberg-constant)
  * [Fine Structure Constant](#fine-structure-constant)
  * [Molar Gas Constant](#molar-gas-constant)
  * [Vacuum Permeability (Magnetic Constant)](#vacuum-permeability--magnetic-constant-)
  * [Wien Frequency Displacement Law Constant](#wien-frequency-displacement-law-constant)
  * [Impedance of Free Space](#impedance-of-free-space)
  * [Newtonian Constant of Gravitation](#newtonian-constant-of-gravitation)
* [Program Tests](#program-tests)
* [Resources](#resources)
  * [Libraries & Documentation](#libraries--documentation)
  * [Physical Constants](#physical-constants)
* [Future Work](#future-work)
* [My Gratitude](#my-gratitude)
<!-- TOC -->

## Motivation & Concept

Most of the physical constants are observed from experiments and measured by instruments within the given error range.

Like Stefan-Boltzmann Constant, [Prof. Dr. Josef Stefan](https://en.wikipedia.org/wiki/Josef_Stefan) had found the relation between radiation power and temperature of the black body radiation problem:

```math
j^{\star} = \sigma T^{4}
```

where,

* $j^{\star}$ is radiated power per unit area
* $T^{4}$ is 4. power of radiated material's temperature 
* $\sigma$ is a __physical constant__ (known as Stefan–Boltzmann constant) 

Theoretical formulation of `σ` was done by [Prof. Dr. Ludwig Eduard Boltzmann](https://en.wikipedia.org/wiki/Ludwig_Boltzmann):

```math
{\displaystyle \sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}} \approxeq 5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}}
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

Formulation of `σ` was [theoretically derived](https://edisciplinas.usp.br/pluginfile.php/48089/course/section/16461/qsp_chapter10-plank.pdf) by using the other physical and mathematical constants.

Now, let's think oppositely amd assume we have a function which takes:

* Target value: 5.670374E-8 (in [Scientific Notation](https://en.wikipedia.org/wiki/Scientific_notation))
* Target unit: $\mathrm{kg}\\times\mathrm{s}^{-3}\\times\mathrm{K}^{-4}$
* List of physical constants with their units ($k$, $h$, $c$, ...)
* List of mathematical constants ($\pi$, $e$, ...)
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
And I know that this methodology can be expanded to a wider scope with distributed calculation methods.

## Methodology

It is a well-known fact that the resultant physical unit on the right side of the equations must match the left side.

This is the main methodology that I have followed:

1. Prepare the candidate list by calculating the combination of physical constants which matched the target unit.
2. Iterate over the candidates, looking for a combination of dimensionless mathematical constants, such that the resulting multiplication places within the desired error range.

![Flowchart of Physical Constants Explorer](./img/Flowchart_of_Physical_Constants_Explorer.drawio.svg)

I wanted to apply a simple and clear set of methodologies:

1. Brute force algorithm for all multiplication combinations
2. Using a unit library ([pint](https://pint.readthedocs.io/en/stable/)) to:
   * Represent physical dimensional constants
   * Convert physical constants and multiplications to base SI units
   * Correctly calculate the multiplication of physical and mathematical constants
3. Using scientific notation with the ["concise form"](https://en.wikipedia.org/wiki/Scientific_notation#Estimated_final_digits) for input target values. 
4. Ignore errors on the right side of the equation, i.e. resultant error of the combination of the calculated multiplications. 
5. Using [decimal](https://docs.python.org/3/library/decimal.html) library to represent numbers with high significant digits (50 is set as default precision)

## Python Installation

The implementation is done by using Python 3.9.13

If python is not installed, I suggest using one of "Python Version Manager" (Anaconda, pyenv, etc.)

Please execute the following code on the projects root folder:

```shell
> python -m venv ./venv
> source ./venv/bin/activate
> python -m pip install --upgrade pip
> pip install -r ./requirements.txt
```

## Running the Program

### Constants Definition File
The program is using [pint](https://pint.readthedocs.io/en/stable/) library to use and operate on physical (dimensional) & mathematical (dimensionless) constants.

You can override to modify [pint default constants definition file](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt).

The overriden file is located [definition/constants_en.txt](definition/constants_en.txt). You can also change this file to add and modify the constant definitions. 

### The Config File 

The config file is required to restrict the program scope. The default [./config.json](config.json)) file and its format:
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

If you do not provide the config file separately in the program, the default [./config.json](config.json)) file is used.

The file holds the constants and their power ranges that the program will consider & calculate.

| Root Setting             | Sub Setting            | Keys                                                                                                                       | Values                                                                                                                                                                                                                              |
|--------------------------|------------------------|----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "physical_constants"     | "method"               |                                                                                                                            | "brute_force"                                                                                                                                                                                                                       |
| "physical_constants"     | "constants_and_powers" | Dimensional physical constant name. It must be defined on [the definition file](./definition/constants_en.txt).            | The power range. <br/>* `Array`: `[min, max]`. The program converts it as integer range e.g. `[min, ..., max]`. It adds `0`, if `0` does not exist in the range.<br/>* `Integer`: the program converts it as `[-value, ..., value]` |
| "mathematical_constants" | "numbers_and_powers"   | Prime numbers in string format e.g. "2"                                                                                    | The power range. The format is the same as above.                                                                                                                                                                                   |
| "mathematical_constants" | "constants_and_powers" | Dimensionless mathematical constant name. It must be defined on [the same definition file](./definition/constants_en.txt). | The power range. The format is the same as above.                                                                                                                                                                                   |
The result of the calculation is represented in terms of `key` values.

### The Program Inputs

The program `main.py` takes target value and unit with the following input names:
* `--target-value` 
* `--target-unit`
* `--config-path` (optional)

As an example, exploring `Rydberg Constant`:
```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m"
```
<br />

Please use `--help` option 
```shell
> python ./main.py --help
```
To get more info about the program usage:
```text
options:
  -h, --help            show this help message and exit
  -v, --target-value 
                        Target value with scientific notation.
                        To specify target value with measurement error:
                        For example (1.23±0.06)×10^−5, please provide it in "concise form" like 1.23(6)E-5.
                        Examples with error: "1.23(6)E-5", "8.9875(15)E+16", "4.2(3)E+0"
                        
                        The target value can also be provided without error specification:
                        Examples without error: "1.23E-5", "8.9875E+16", "4.2E+0"
                        If you provide target value without error, it equals to:
                        "1.23E-5" ≈ "1.235(5)E-5"
  -u, --target-unit 
                        Target unit expression in terms of SI base units symbols.
                        Length - meter (m)
                        Time - second (s)
                        Amount of substance - mole (mol)
                        Electric current - ampere (A)
                        Temperature - kelvin (K)
                        Luminous intensity - candela (cd)
                        Mass - kilogram (kg)
                        Use ^ symbol to represent power.
                        Examples: "kg/(s^3 K^4)", "kg s^-3 K^-4", "m/s"
  -c, --config-path 
                        Config file relative path.
                        If it is not provided the program will try to read ./config.json
```

## Exploring Well-known Physical Constants

The [script](scripts/analyse_all.sh) below executed the following physical constants and stored the results.

```shell
> ./scripts/analyse_all.sh
```

### Stefan Boltzmann Constant

```shell
> python ./main.py --target-value "5.670374419E-8" --target-unit "kg/(s^3 K^4)"
```
* [The output of the program](scripts/outputs/analyse_all/stefan_boltzmann_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?sigma|search_for=stefan)
* [More info about the constant](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant)

### Rydberg Constant

```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m"
```
* [The output of the program](scripts/outputs/analyse_all/rydberg_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?ryd|search_for=rydberg+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Rydberg_constant)

### Fine Structure Constant

```shell
> python ./main.py --target-value "7.2973525693(11)E-3" --target-unit ""
```
* [The output of the program](scripts/outputs/analyse_all/fine_structure_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?alph|search_for=fine+structure+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Fine-structure_constant)

### Molar Gas Constant

```shell
> python ./main.py --target-value "8.314462618E0" --target-unit "(kg m^2)/(K mol s^2)"
```
* [The output of the program](scripts/outputs/analyse_all/molar_gas_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?r|search_for=molar+gas+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Gas_constant)

### Vacuum Permeability (Magnetic Constant)

```shell
> python ./main.py --target-value "1.25663706212(19)e-6" --target-unit "m kg/(A^2 s^2)"
```
* [The output of the program](scripts/outputs/analyse_all/magnetic_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?mu0|search_for=vacuum+permeability)
* [More info about the constant](https://en.wikipedia.org/wiki/Vacuum_permeability)

### Wien Frequency Displacement Law Constant

```shell
> python ./main.py --target-value "5.878925757E+10" --target-unit "1/(K s)"
```
* [The output of the program](scripts/outputs/analyse_all/wien_frequency_displacement_law_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?bpwien|search_for=wien_frequency+displacement+law+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Wien%27s_displacement_law)

### Impedance of Free Space

```shell
> python ./main.py --target-value "3.76730313668(57)E+2" --target-unit "(kg m^2)/(s^3 A^2)"
```
* [The output of the program](scripts/outputs/analyse_all/impedance_of_free_space.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?z0|search_for=characteristic+impedance+of+vacuum)
* [More info about the constant](https://en.wikipedia.org/wiki/Impedance_of_free_space)

### Newtonian Constant of Gravitation

```shell
> python ./main.py --target-value "6.67430(15)e-11" --target-unit "m^3/(kg s^2)"
```
* [The output of the program](scripts/outputs/analyse_all/newtonian_constant_of_gravitation.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?bg|search_for=newtonian+constant+of+gravitation)
* [More info about the constant](https://en.wikipedia.org/wiki/Gravitational_constant)

Unfortunately, there is no meaningfully results are found for `Newtonian Constant of Gravitation` yet!

## Program Tests

Test folder is [here](src/tests). To run the all test:

```shell
> pytest
```

## Resources

### Libraries & Documentation
* [pint](https://pint.readthedocs.io/en/stable/)
  * [pint repo](https://github.com/hgrecco/pint/tree/master/pint)
  * [pint default constants definition file](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt)
  * [pint developer reference](https://pint.readthedocs.io/en/stable/developers_reference.html)
  * [pint tutorıal](https://pint.readthedocs.io/en/stable/tutorial.html)
* [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
* [Latex Mathematics](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
  * [Writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)

### Physical Constants
* [The NIST Reference on Constants, Units, and Uncertainty](https://physics.nist.gov/cuu/Constants/index.html)
* [NIST, Fundamental Physical Constants — Extensive Listing](https://physics.nist.gov/cuu/pdf/all.pdf)

## Future Work

* Is it possible to find all (known) physical constants with a single config file? Targeting `1.0000` with `dimensionless`, methodology can be usefully for this purpose, like:
```shell
> python ./main.py --target-value "1.00000E+0" --target-unit ""
```

* Implement error calculation on multiplications & in the definition file. [uncertainties library](https://uncertainties-python-package.readthedocs.io/en/latest/) can be a good candidate! 
* Since only `Boltzman` constant has `K` Kelvin dimension space in its unit, check another independent physical constant which contains `K` on its units!

## Gratitudes

I would like to express my gratitude to my teachers:
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

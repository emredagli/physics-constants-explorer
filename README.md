# Physics Constants Explorer

This repo contains the research to find the physics constant formulations numerically in terms of other physical & mathematical constants.

## Motivation & Concept

Most of the physical constants are observed from experiments & measured by devices within the given error range.

Like Stefan-Boltzmann Constant, [Mr. Josef Stefan](https://en.wikipedia.org/wiki/Josef_Stefan) had found the relation between power and temperature of black body radiation:

```math
j^{\star} = \sigma T^{4}
```

Theoretical formulation of σ was done by [Mr. Ludwig Eduard Boltzmann](https://en.wikipedia.org/wiki/Ludwig_Boltzmann):

```math
{\displaystyle \sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}}=5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}}
```

where

* k is the [Boltzmann constant](https://en.wikipedia.org/wiki/Boltzmann_constant) (physical constant)
* h is the [Planck constant](https://en.wikipedia.org/wiki/Planck_constant) (physical constant)
* c is the speed of light in vacuum (physical constant)
* π is the ratio of a circle's circumference to its diameter (mathematical constant)

with SI base units:

* kg is kilogram
* s is second
* K is Kelvin

So as you see, σ was [theoretically proofed](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law) & formulated by the other physical & mathematical constants.

Now, let's think oppositely & assume we have a function which takes:

* Target value: 5.67037E-8
* Target unit: $\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}$
* List of physical constants with their units & their power range (k, h, c, ...)
* List of mathematical constants & their power range (π, e, ...)
* List of prime numbers & their power range (2, 3, 5, ...)

and returns the matched formula(s), so that:

* the target unit is "exactly" matched with the unit of formula and,
* the target value is matched with the resultant numeric value (with in the same significant digit of the target).

For example:
Input: 
```
target_value = "5.670374E-8" 
target_unit = "kg/(s^3 K^4)"
```
Output:
```
2⋅pi⁵⋅k⁴ / (3⋅5⋅c²⋅h³)
```

Would it be possible & useful?

Yes it is possible. To be honest, I am not definitely sure about its usefulness!

But I would like to start this study with the excitement of opportunity of being the first person to see the possible formulation of some famous physical constants.

## Methodology

All my Physics teacher and the lecturers in Pysics Department, said that the resultant physical unit on the right and left side of the equations must be the same.

This is the main methodology that I have followed:

1. Find the multiplication of physical constants which matched the target unit
2. Search the combination of the prime numbers & mathematical constant multiplications so that target value is within the error range.

I wanted to start with a simple and clear methodologies:

1. Brute force algorithm for all multiplication combinations
2. Using a unit library [pint](https://pint.readthedocs.io/en/stable/) to:
   * Represent physical constants
   * Convert physical constants & multiplications to base SI units
   * Correctly calculate the multiplication of physical & mathematical constants
3. Using dictionaries to:
   * Hold precalculated multiplication of prime numbers & mathematical constants
   * Speed up fetching the multiplication results as O(1)
4. Using [decimal](https://docs.python.org/3/library/decimal.html) & [fractions](https://docs.python.org/3/library/fractions.html) libraries to
   * Represent prime number multiplications
   * Not to use `float` type (which has max 15 decimal precision) in `pint` library

## Install

The implementation is done by using Python 3.9.13

If python is not installed, I suggest using one of "Python Version Manager" (Anaconda, pyenv, etc.)

Please execute the following code on the project root folder:

```shell
> python -m venv ./venv
> source ./venv/bin/activate
> python -m pip install --upgrade pip
> pip install -r ./requirements.txt
```

The shell code above is doing pretty standard Python initialization for a project:

* creates a virtual env. in which you can install dependencies separately
* source the created virtual environment under the `./venv` folder
* update the pip - package manager
* install the dependant libraries

## Run the Program

### Configuration
The program is using 2 files:

* Physical & mathematical constants definition file: [definition/constants_en.txt](definition/constants_en.txt)
* The config file: [config.json](config.json)

The config file format in JSON:
```json
{
  "physical_constants": {
    "method": "brute_force",
    "constants_and_powers": {
      "speed_of_light": 4,
       ...
    }
  },
  "mathematical_constants": {
    "numbers_and_powers": {
      "2": 5,
      ...
    },
    "constants_and_powers": {
      "pi": 5,
      "eulers_number": 5
    }
  }
}
```

The config file has:

"`key`" (string): `value` (integer) pairs. 

The `value` part defines max power value. The program calculates & considers `[-value, ..., value]` integer power ranges.

The result of the calculation is represented in terms of `key` values & powers in the given ranges (the last line of the output [stefan_boltzmann_constant.txt](scripts/outputs/analyse_all/stefan_boltzmann_constant.txt))

The file composed of:
* `physical_constants`, contains __dimensional__ physical constants.
  * `constants_and_powers`
    * `key` values must be defined under [the definition file](definition/constants_en.txt).
* `mathematical_constants`, contains __dimensionless__ mathematical values & constants
  * `numbers_and_powers`
    * `key` values are prime numbers
  * `constants_and_powers`
    * `key` values must be defined under [the same definition file](definition/constants_en.txt) given above.


### Run the Program

The program `main.py` uses the configuration file explained above and takes target input:
* `-v` (or `--target-value`)
* `-u` (or `--target-unit`)

For example:
```shell
> python main.py --target-value "5.670374E-8" --target-unit "kg/(s^3 K^4)"
```

To get more info about the usage & input formats:
```shell
> python main.py --help
```

Displays:
```text
options:
  -h, --help            show this help message and exit
  -v, --target-value 
                        Target value with scientific notation.
                        Examples: "5.6560E-8", "8.9875517873681764E+16", "1.000042E+0"
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
```

### Exploring Well-known Physical Constants

```shell
> ./scripts/analyse_all.sh
```

The script above executes the following physical constants and stores the results:

* [Stefan Boltzmann Constant](scripts/outputs/analyse_all/stefan_boltzmann_constant.txt)
* [Rydberg Constant](scripts/outputs/analyse_all/rydberg_constant.txt)
* [Fine Structure Constant](scripts/outputs/analyse_all/fine_structure_constant.txt)
* [Newtonian Constant of Gravitation](scripts/outputs/analyse_all/newtonian_constant_of_gravitation.txt)
* [Molar Gas Constant](scripts/outputs/analyse_all/molar_gas_constant.txt)
* [Vacuum Permeability](scripts/outputs/analyse_all/vacuum_permeability.txt)

## Tests

Test folder is [here](src/tests). You can run tests on the project root:

```shell
> pytest
```

## Dev Resources

### Libraries & Documentation
* [pint](https://pint.readthedocs.io/en/stable/)
  * [pint repo](https://github.com/hgrecco/pint/tree/master/pint)
  * [Default Pint constants definition file](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt)
  * [pint Developer reference](https://pint.readthedocs.io/en/stable/developers_reference.html)
  * [pint tutorıal](https://pint.readthedocs.io/en/stable/tutorial.html)
* [Latex Mathematics](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
  * [Writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)

### Physical Constants
* [Fundamental Physical Constants](https://www.ge.infn.it/apetrolini/FisGen/doc-fis2-01.pdf)


## My Gratitude  

I would like to express my gratitude to my teachers:

* Physics Teacher Aykut Gumuc (R.I.P), Eskisehir Science High School, EFFL
* Prof. Dr. Oleg Fedorovich Kabardin (R.I.P), International Physics Olympiad (IPhO)
* Prof. Dr. İbrahim Günal (R.I.P), METU-Physics
* Prof. Dr. Ordal Demokan (R.I.P), METU-Physics
* Physics Teacher Rafet Kamer, International Physics Olympiad (IPhO)
* Prof. Dr. K. Sinan Bilikmen, METU-Physics
* Prof. Dr. Mehmet Tomak, METU-Physics
* Prof. Dr. Göktürk Üçoluk, METU-Computer Engineering
* Prof. Dr. Ali Demirsoy, Hacettepe University

& to my genius and big-hearted friends who always enjoy supporting me:
* Dr. İnanç Kanık
* Dr. Özgür Sümer
* Atılım Çetin
* Osman Özgür

& to my dear wife Ayşen and my dear children Ozan & Doruk!

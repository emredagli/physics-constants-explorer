# Physics Constants Explorer

This work contains research to find physical constants numerically in terms of other physical & mathematical constants within a given scope.

## Motivation & Concept

Most of the physical constants are observed from experiments & measured by devices within the given error range.

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
{\displaystyle \sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}}=5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}}
```

where

* $k$ is the [Boltzmann constant](https://en.wikipedia.org/wiki/Boltzmann_constant) (another physical constant)
* $h$ is the [Planck constant](https://en.wikipedia.org/wiki/Planck_constant) (another physical constant)
* $c$ is the speed of light in vacuum (another physical constant)
* π is the ratio of a circle's circumference to its diameter (mathematical constant)

with SI base units:

* kg is kilogram
* s is second
* K is Kelvin

Formulation of `σ` was [theoretically derived](https://edisciplinas.usp.br/pluginfile.php/48089/course/section/16461/qsp_chapter10-plank.pdf) by using the other physical & mathematical constants.

Now, let's think oppositely & assume we have a function which takes:

* Target value: 5.670374E-8
* Target unit: $\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}$
* List of physical constants with their units & their power range (k, h, c, ...)
* List of mathematical constants & their power range (π, e, ...)
* List of prime numbers & their power range (2, 3, 5, ...)

and returns the matched formula(s), so that:

* the target unit is "exactly" matched with the unit of formula and,
* the target value is matched with the resultant numeric value (with in the same significant digit of the target).

For example, input is: 
```
target_value = "5.670374E-8" 
target_unit = "kg/(s^3 K^4)"
```

And the output:
```
2 ⋅ pi⁵ ⋅ boltzmann_constant⁴ / (3 ⋅ 5 ⋅ speed_of_light² ⋅ planck_constant³)
```

Would it be possible & useful?

Yes it is possible. To be honest, I am not definitely sure about its usefulness!

But I would like to start this study with the excitement of opportunity of being the first person to see the possible formulation of some famous physical constants.

And I know that this methodology can be expanded to wider scope with distributed calculation methods.

## Methodology

It is a well-known fact that the resultant physical unit on the right side of the equations must match the left side.

This is the main methodology that I have followed:

1. Prepare the candidate list by calculating the combination of physical constants which matched the target unit.
2. Iterate the candidates, looking for a combination of dimensionless mathematical constants, such that the resulting multiplication places within the desired error range.

I wanted to start with a simple and clear methodologies:

1. Brute force algorithm for all multiplication combinations
2. Using a unit library ([pint](https://pint.readthedocs.io/en/stable/)) to:
   * Represent physical dimensional constants
   * Convert physical constants & multiplications to base SI units
   * Correctly calculate the multiplication of physical & mathematical constants
3. Using [decimal](https://docs.python.org/3/library/decimal.html) library to
   * Represent numbers with high significant digits (50 is set as default precision)
4. Truncating the resultant multiplication to the target precision to check error range

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

* Constants definition file: [definition/constants_en.txt](definition/constants_en.txt)
* The config file: [config.json](config.json)

The config file format in JSON:
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
      "2": [-4, 4],
      ...
    },
    "constants_and_powers": {
      "pi": [-5, 5],
      "eulers_number": [-5, 5]
    }
  }
}
```

The config file format:

| Root Setting           | Sub Setting          | Key                                                                                                                        | Value                                                                                                                                                                                                                                                                                                                                              |
|------------------------|----------------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| physical_constants     | method               |                                                                                                                            | The only value: "brute_force".                                                                                                                                                                                                                                                                                                                     |
| physical_constants     | constants_and_powers | Dimensional physical constant name. It must be defined on [the definition file](./definition/constants_en.txt).            | The value represents the power range. You can provide this value with 2 ways:<br/>* `Array`: `[min, max]`. The program converts it as all integer values in this range e.g. `[min, ..., max]`. It adds `0` into the power range, if `0` does not exist in the calculated range.<br/>* `Integer`: the program converts it as `[-value, ..., value]` |
| mathematical_constants | numbers_and_powers   | Prime numbers in string format like "2"                                                                                    | The value represents the power range. The format is the same as above.                                                                                                                                                                                                                                                                             |
| mathematical_constants | constants_and_powers | Dimensionless mathematical constant name. It must be defined on [the same definition file](./definition/constants_en.txt). | The value represents the power range. The format is the same as above.                                                                                                                                                                                                                                                                             |



The result of the calculation is represented in terms of `key` values (please check a result on the last line [stefan_boltzmann_constant.txt](scripts/outputs/analyse_all/stefan_boltzmann_constant.txt))


### Run the Program

The program `main.py` uses the configuration file explained above and takes target input:
* `-v` (or `--target-value`)
* `-u` (or `--target-unit`)

For example:
```shell
> python main.py --target-value "5.670374E-8" --target-unit "kg/(s^3 K^4)"
```

To get more info about the program usage & input formats:
```shell
> python main.py --help
```

Displays:
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

### Exploring Well-known Physical Constants

```shell
> ./scripts/analyse_all.sh
```

The [script](scripts/analyse_all.sh) above executes the following physical constants and stores the results.

Found results:
* [Stefan Boltzmann Constant](scripts/outputs/analyse_all/stefan_boltzmann_constant.txt)
* [Rydberg Constant](scripts/outputs/analyse_all/rydberg_constant.txt)
* [Fine Structure Constant](scripts/outputs/analyse_all/fine_structure_constant.txt)
* [Molar Gas Constant](scripts/outputs/analyse_all/molar_gas_constant.txt)
* [Magnetic Constant (Vacuum Permeability)](scripts/outputs/analyse_all/magnetic_constant.txt)
* [Wien Frequency Displacement Law Constant](scripts/outputs/analyse_all/wien_frequency_displacement_law_constant.txt)
* [Impedance of Free Space](scripts/outputs/analyse_all/impedance_of_free_space.txt)


Not found results:
* [Newtonian Constant of Gravitation](scripts/outputs/analyse_all/newtonian_constant_of_gravitation.txt)

Notes about [config.json](config.json) file while calculating these constants:
* config.json file expanded progressively to cover all constants above
* Since there is a [direct relation](https://en.wikipedia.org/wiki/Speed_of_light#Propagation_of_light) between speed of light, electric constant $\varepsilon _{0}$ and the magnetic constant $\mu _{0}$ 

```math
{\displaystyle c={\frac {1}{\sqrt {\varepsilon _{0}\mu _{0}}}}\ .}
```

only "electric_constant" is included into the config.json file to reduce the resultant space on the analysis above.


## Tests

Test folder is [here](src/tests). You can run tests on the project root:

```shell
> pytest
```

## Dev Resources

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
* [Fundamental Physical Constants — Extensive Listing](https://physics.nist.gov/cuu/pdf/all.pdf)
* [Fundamental Physical Constants - https://physics.nist.gov/](https://physics.nist.gov/cuu/Constants/index.html)

## TODOs

* Implement error calculation on multiplications. [uncertainties library](https://uncertainties-python-package.readthedocs.io/en/latest/) seems to be a good candidate 

## My Gratitude  

I would like to express my gratitude to my teachers:

* Prof. Dr. İbrahim Günal (R.I.P), METU-Physics
* Prof. Dr. Ordal Demokan (R.I.P), METU-Physics
* Physics Teacher Aykut Gümüç (R.I.P), Eskisehir Science High School
* Prof. Dr. Oleg Fedorovich Kabardin (R.I.P), Physics Olympiads


* Physics Teacher Rafet Kamer, Physics Olympiads
* Prof. Dr. K. Sinan Bilikmen, METU-Physics
* Prof. Dr. Mehmet Tomak, METU-Physics


& to my genius and big-hearted friends who always enjoy supporting me:
* Dr. İnanç Kanık
* Dr. Özgür Sümer
* Atılım Çetin
* Osman Özgür

& to my dear wife Ayşen and my dear children Ozan & Doruk!

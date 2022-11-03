# Physics Constants Explorer

This work contains research and a python program to explore physical constants formulation in terms of given other physical & mathematical constants.

<!-- TOC -->

* [Motivation & Concept](#motivation--concept)
* [Methodology](#methodology)
* [Python Installation](#python-installation)
* [Running the Program](#running-the-program)
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
  * [Josephson Constant](#josephson-constant)
  * [Von Klitzing Constant](#von-klitzing-constant)
* [Exploring Measured But Unknown Physical Constants](#exploring-measured-but-unknown-physical-constants)
  * [Magnetic Constant to Electric Constant Ratio](#magnetic-constant-to-electric-constant-ratio)
  * [Newtonian Constant of Gravitation (G)](#newtonian-constant-of-gravitation--g-)
    * [First Attempt](#first-attempt)
    * [Second Attempt](#second-attempt)
* [Tests](#tests)
* [Resources](#resources)
  * [Libraries & Documentation](#libraries--documentation)
  * [Physical Constants](#physical-constants)
* [Future Work](#future-work)
* [Gratitude](#gratitude)

<!-- TOC -->

## Motivation & Concept

Most of the relations in physics are observed from experiments and constants in the relations measured by instruments within the given error range.

For example Stefan-Boltzmann Constant, [Prof. Dr. Josef Stefan](https://en.wikipedia.org/wiki/Josef_Stefan) had found the relation between radiation power and temperature of the black body radiation problem:

$$j^{\star} = \sigma T^{4}$$

where,

* $j^{\star}$ is radiated power per unit area
* $T^{4}$ is 4. power of radiated material's temperature
* $\sigma$ is a __physical constant__ (known as Stefan–Boltzmann constant)

Theoretical formulation of $\sigma$ was done by [Prof. Dr. Ludwig Eduard Boltzmann](https://en.wikipedia.org/wiki/Ludwig_Boltzmann):

$$\sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}} \approxeq 5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}$$

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
| "physical_constants"                                                  | "constants_and_powers" | Dimensional physical constant name. It must be defined on[the definition file](./definition/constants_en.txt).            | The power range.<br/>* `Array`: `[min, max]`. The program converts it as integer range e.g. `[min, ..., max]`. It adds `0`, if `0` does not exist in the range.<br/>* `Integer`: the program converts it as `[-value, ..., value]` |
| "mathematical_constants"                                              | "numbers_and_powers"   | Prime numbers in string format e.g. "2"                                                                                   | The power range. The format is the same as above.                                                                                                                                                                                  |
| "mathematical_constants"                                              | "constants_and_powers" | Dimensionless mathematical constant name. It must be defined on[the same definition file](./definition/constants_en.txt). | The power range. The format is the same as above.                                                                                                                                                                                  |
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
                        Some examples: "1.23E-5", "8.9875E+16", "4.2E+0"
                        The program converts "1.23E-5" to "1.235(5)E-5"
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
  -c, --config-path 
                        Config file relative path.
                        If it is not provided the program will use default config file: config/config.json
```

## Exploring Well-known Physical Constants

The script ([analyse_all.sh](scripts/analyse_all.sh)) executed the all physical constants explorations given on this document and stored the results.

```shell
> ./scripts/analyse_all.sh
```

[CODATA](https://physics.nist.gov/cuu/Constants/international.html) values are used as `--target-value` in concise form if a measurement error is specified.

### Stefan Boltzmann Constant

$$\sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}} \approxeq 5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}$$

```shell
> python ./main.py --target-value "5.670374419E-8" --target-unit "kg/(s^3 K^4)"
...
Result(s) matched the target:
	(5.6703744195 ± 0.0000000005)✕10⁻⁸ kg/K⁴/s³
	 5.6703744192✕10⁻⁸ kg/K⁴/s³ ≈ 2 ⋅ pi⁵ ⋅ boltzmann_constant⁴ / (3 ⋅ 5 ⋅ speed_of_light² ⋅ planck_constant³)
```

* [The output of the program](scripts/outputs/analyse_all/stefan_boltzmann_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?sigma|search_for=stefan)
* [More info about the constant](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant)

On the output of the program,

```text
...
Found 3 candidates the resultant unit matched with the target's unit:
	[ M ] [ kg/K⁴/s³ ] = boltzmann_constant⁴ / (speed_of_light² ⋅ planck_constant³)
	  ├── 👍 In range!
	  └──  Min (~5✕10⁻¹³) < M̲ ̲(̲~̲1̲✕̲1̲0̲⁻̲⁹̲)̲ < Max (~6✕10⁻³) 

	[ M ] [ kg/K⁴/s³ ] = boltzmann_constant⁴ ⋅ electric_constant / (speed_of_light ⋅ planck_constant² ⋅ elementary_charge²)
	  ├── 👍 In range!
	  └──  Min (~5✕10⁻¹³) < M̲ ̲(̲~̲1̲✕̲1̲0̲⁻̲⁷̲)̲ < Max (~6✕10⁻³) 

	[ M ] [ kg/K⁴/s³ ] = boltzmann_constant⁴ ⋅ electric_constant² / (planck_constant ⋅ elementary_charge⁴)
	  ├── 👍 In range!
	  └──  Min (~5✕10⁻¹³) < M̲ ̲(̲~̲7̲✕̲1̲0̲⁻̲⁶̲)̲ < Max (~6✕10⁻³) 
...
```

The program calculated physical constant multiplications and represented its numerical value as `[ M ]`.

```text
...
	  └──  Min (~5✕10⁻¹³) < M̲ ̲(̲~̲1̲✕̲1̲0̲⁻̲⁹̲)̲ < Max (~6✕10⁻³)
...
Here, the values inside of the brackets represent:
M̲ ̲(̲...)̲ = The multiplication of physical constants
Min (...) = Target value / [The maximum value of the mathematical multiplication combinations]
Max (...) = Target value / [The minimum value of the mathematical multiplication combinations]
```

And finally,

```text
	  ├── 👍 In range!
Highlights the candidate M value is in Min (...) and Max (...) range.
```

### Rydberg Constant

$$R_{\infty }={\frac {m_{\text{e}}e^{4}}{8\varepsilon _{0}^{2}h^{3}c}}$$

```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m"
...
Result(s) matched the target:
	(1.0973731568160 ± 0.0000000000021)✕10⁷ 1/m
	 1.0973731568160✕10⁷ 1/m ≈ elementary_charge⁴ ⋅ electron_mass / (2³ ⋅ speed_of_light ⋅ planck_constant³ ⋅ electric_constant²)
```

* [The output of the program](scripts/outputs/analyse_all/rydberg_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?ryd|search_for=rydberg+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Rydberg_constant)

### Fine Structure Constant

$$\alpha ={\frac {e^{2}}{2\varepsilon _{0}hc}}$$

```shell
> python ./main.py --target-value "7.2973525693(11)E-3" --target-unit ""
...
Result(s) matched the target:
	(7.2973525693 ± 0.0000000011)✕10⁻³ dimensionless
	 7.2973525693✕10⁻³  ≈ elementary_charge² / (2 ⋅ speed_of_light ⋅ planck_constant ⋅ electric_constant)
```

* [The output of the program](scripts/outputs/analyse_all/fine_structure_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?alph|search_for=fine+structure+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Fine-structure_constant)

### Molar Gas Constant

$$R=N_{\rm {A}}k_{\rm {B}}$$

```shell
> python ./main.py --target-value "8.314462618E0" --target-unit "(kg m^2)/(K mol s^2)"
...
Result(s) matched the target:
	(8.3144626185 ± 0.0000000005) kg·m²/K/mol/s²
	 8.3144626182✕10⁰ kg·m²/K/mol/s² ≈ boltzmann_constant ⋅ avogadro_constant
```

* [The output of the program](scripts/outputs/analyse_all/molar_gas_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?r|search_for=molar+gas+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Gas_constant)

### Vacuum Permeability (Magnetic Constant)

$$\mu _{0}={1 \over {c^{2}\varepsilon _{0}}}$$

```shell
> python ./main.py --target-value "1.25663706212(19)e-6" --target-unit "m kg/(A^2 s^2)"
...
Result(s) matched the target:
	(1.25663706212 ± 0.00000000019)✕10⁻⁶ kg·m/A²/s²
	 1.25663706213✕10⁻⁶ kg·m/A²/s² ≈ 1 / (speed_of_light² ⋅ electric_constant)
```

* [The output of the program](scripts/outputs/analyse_all/magnetic_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?mu0|search_for=vacuum+permeability)
* [More info about the constant](https://en.wikipedia.org/wiki/Vacuum_permeability)

### Wien Frequency Displacement Law Constant

$$\nu _{\text{peak}}={\alpha  \over h}kT\approx (5.879\times 10^{10}\ \mathrm {Hz/K} )\cdot T$$

```shell
> python ./main.py --target-value "5.878925757E+10" --target-unit "1/(K s)"
...
Result(s) matched the target:
	(5.8789257575 ± 0.0000000005)✕10¹⁰ 1/K/s
	 5.8789257576✕10¹⁰ 1/K/s ≈ wien_u ⋅ boltzmann_constant / planck_constant
```

* [The output of the program](scripts/outputs/analyse_all/wien_frequency_displacement_law_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?bpwien|search_for=wien_frequency+displacement+law+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Wien%27s_displacement_law#Frequency-dependent_formulation)

### Impedance of Free Space

$$Z_{0}={\frac {E}{H}}=\mu _{0}c={\sqrt {\frac {\mu _{0}}{\varepsilon _{0}}}}={\frac {1}{\varepsilon _{0}c}}$$

```shell
> python ./main.py --target-value "3.76730313668(57)E+2" --target-unit "(kg m^2)/(s^3 A^2)"
...
Result(s) matched the target:
	(3.76730313668 ± 0.00000000057)✕10² kg·m²/A²/s³
	 3.76730313668✕10² kg·m²/A²/s³ ≈ 1 / (speed_of_light ⋅ electric_constant)
```

* [The output of the program](scripts/outputs/analyse_all/impedance_of_free_space.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?z0|search_for=characteristic+impedance+of+vacuum)
* [More info about the constant](https://en.wikipedia.org/wiki/Impedance_of_free_space#Relation_to_other_constants)

### Josephson Constant

$$1 / \Phi _{B}={\frac {2e}{h}}$$

```shell
> python ./main.py --target-value "4.835978484E+14" --target-unit "(A s^2)/(kg m^2)"
...
Result(s) matched the target:
	(4.8359784845 ± 0.0000000005)✕10¹⁴ A·s²/kg/m²
	 4.8359784842✕10¹⁴ A·s²/kg/m² ≈ 2 ⋅ elementary_charge / planck_constant
```

* [The output of the program](scripts/outputs/analyse_all/josephson_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?kjos|search_for=josephson)
* [More info about the constant](https://en.wikipedia.org/wiki/Magnetic_flux_quantum)

### Von Klitzing Constant

$$\R_{K}={\frac {h}{e^{2}}}$$

```shell
> python ./main.py --target-value "2.581280745E+4" --target-unit "(kg m^2)/(A^2 s^3)"
...
Result(s) matched the target:
	(2.5812807455 ± 0.0000000005)✕10⁴ kg·m²/A²/s³
	 2.5812807459✕10⁴ kg·m²/A²/s³ ≈ planck_constant / elementary_charge²
```

* [The output of the program](scripts/outputs/analyse_all/von_klitzing_constant.txt)
* [Target value reference](https://physics.nist.gov/cgi-bin/cuu/Value?rk|search_for=von+Klitzing+constant)
* [More info about the constant](https://en.wikipedia.org/wiki/Quantum_Hall_effect#Applications)

## Exploring Measured But Unknown Physical Constants

After executing enough runs on the well-known physical constants, it is time to experiment on measured but not theoretically-proofed constants.

Before making the experiments, I have added the following square root [definitions](definition/constants_en.txt) to increase the search space in unit dimension:

* sqrt_speed_of_light = speed_of_light ** 0.5
* sqrt_planck_constant = planck_constant ** 0.5
* sqrt_electron_mass = electron_mass ** 0.5
* ...

And on the results, I have removed to `sqrt_` prefix for even powers by dividing the power by 2.

Rather than giving direct results, I would like to explain how the final results were found:

### Magnetic Constant to Electric Constant Ratio

Definitions:

* $\mu _{0}$, [Vacuum permeability (Magnetic Constant)](https://en.wikipedia.org/wiki/Vacuum_permeability)
  $\mu _{0}=1.25663706212(19) \times 10^{-6} \, \mathrm{kg} \, \mathrm{m} \, \mathrm{A}^{-2} \, \mathrm{s}^{-2}$ ([CODATA value](https://physics.nist.gov/cgi-bin/cuu/Value?mu0|search_for=Vacuum+permeability))
* $\varepsilon _{0}$, [Vacuum permittivity (Electric Constant)](https://en.wikipedia.org/wiki/Vacuum_permittivity)
  $\varepsilon _{0}=8.8541878128(13) \times 10^{-12} \,\mathrm{A^{2}}\,\mathrm{s}^{4}\,\mathrm{kg}^{-1}\,\mathrm{m}^{-3}$ ([CODATA value](https://physics.nist.gov/cgi-bin/cuu/Value?ep0|search_for=Vacuum+permittivity))

The target of this work is exploring the ratio of $\mu _{0} / \varepsilon _{0}$.

The following equations are the well-known relations that contain $\varepsilon _{0}$ and $\mu _{0}$:

(1) c ([speed of light in vacuum](https://en.wikipedia.org/wiki/Speed_of_light#Propagation_of_light)) contains $\varepsilon _{0}$ and $\mu _{0}$:

$$c={\frac {1}{\sqrt {\varepsilon _{0}\mu _{0}}}}$$

(2) $\alpha$ ([fine-structure constant](https://en.wikipedia.org/wiki/Fine-structure_constant)) contains $e$ (elementary charge), $h$ (plank constant), $\varepsilon _{0}$:

$$\alpha={\frac {e^{2}}{2\varepsilon _{0}hc}}={\frac {e^{2}}{2h}}{\sqrt{\frac {\mu _{0}}{\varepsilon _{0}}}}$$

(3) $R_{\infty }$ ([Rydberg constant](https://en.wikipedia.org/wiki/Rydberg_constant)) contains $e$, $m_{\text{e}}$ (the rest mass of the electron), $h$, c:

$$R_{\infty }={\frac {m_{\text{e}}e^{4}}{8\varepsilon _{0}^{2}h^{3}c}}={\frac {m_{\text{e}}e^{4}c}{8h^{3}}}{\frac {\mu _{0}}{\varepsilon _{0}}}$$

The goal is to find the relations given above and by targeting $\mu _{0}/\varepsilon _{0}$ ratio:

$${\frac {\mu _{0}}{\varepsilon _{0}}}=1.4192572923(42) \times 10^{5} \, \mathrm{kg}^{2} \, \mathrm{m}^{4} \, \mathrm{A}^{-4} \, \mathrm{s}^{-6} $$

The error of the ratio is calculated based on the relative errors.

```shell
> python ./main.py --target-value "1.4192572923(42)E+5" \
                   --target-unit "(kg^2 m^4)/(A^4 s^6)" \
                   --config-path "./config/config_mc_to_ec_ratio.json" \
                   > ./scripts/outputs/analyse_all/mc_to_ec_ratio.txt
```

The program found 5 candidates ([output file](scripts/outputs/analyse_all/mc_to_ec_ratio.txt)) that the resultant unit matched with the target's unit with [config_mc_to_ec_ratio.json config file](config/config_mc_to_ec_ratio.json):

```text
	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = planck_constant³ ⋅ rydberg_constant / (speed_of_light ⋅ elementary_charge⁴ ⋅ electron_mass)
	  ├── 👍 In range!
	  └──  Min (~1✕10⁻⁹) < M̲ ̲(̲~̲2̲✕̲1̲0̲⁴̲)̲ < Max (~1✕10¹⁹) 

	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = sqrt_planck_constant⁵ ⋅ sqrt_rydberg_constant / (sqrt_speed_of_light ⋅ elementary_charge⁴ ⋅ sqrt_electron_mass)
	  ├── 👍 In range!
	  └──  Min (~1✕10⁻⁹) < M̲ ̲(̲~̲3̲✕̲1̲0̲⁶̲)̲ < Max (~1✕10¹⁹) 

	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = planck_constant² / elementary_charge⁴
	  ├── 👍 In range!
	  └──  Min (~1✕10⁻⁹) < M̲ ̲(̲~̲7̲✕̲1̲0̲⁸̲)̲ < Max (~1✕10¹⁹) 

	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = sqrt_speed_of_light ⋅ sqrt_planck_constant³ ⋅ sqrt_electron_mass / (elementary_charge⁴ ⋅ sqrt_rydberg_constant)
	  ├── 👍 In range!
	  └──  Min (~1✕10⁻⁹) < M̲ ̲(̲~̲1̲✕̲1̲0̲¹̲¹̲)̲ < Max (~1✕10¹⁹) 

	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = speed_of_light ⋅ planck_constant ⋅ electron_mass / (elementary_charge⁴ ⋅ rydberg_constant)
	  ├── 👍 In range!
	  └──  Min (~1✕10⁻⁹) < M̲ ̲(̲~̲3̲✕̲1̲0̲¹̲³̲)̲ < Max (~1✕10¹⁹) 
```

And 3 of these numerically matched the target value:

```text
Result(s) matched the target:
    (1.4192572923 ± 0.0000000042)✕10⁵ kg²·m⁴/A⁴/s⁶
R1)  1.4192572924✕10⁵ kg²·m⁴/A⁴/s⁶ ≈ 2³ ⋅ planck_constant³ ⋅ rydberg_constant / (speed_of_light ⋅ elementary_charge⁴ ⋅ electron_mass)
R2)  1.4192572924✕10⁵ kg²·m⁴/A⁴/s⁶ ≈ sqrt_2⁵ ⋅ fine_structure_constant ⋅ sqrt_planck_constant⁵ ⋅ sqrt_rydberg_constant / (sqrt_speed_of_light ⋅ elementary_charge⁴ ⋅ sqrt_electron_mass)
R3)  1.4192572924✕10⁵ kg²·m⁴/A⁴/s⁶ ≈ 2² ⋅ fine_structure_constant² ⋅ planck_constant² / elementary_charge⁴
```

As you see:

* result (R1) can be derived from (3) $R_{\infty }$, Rydberg constant formulation given above
* result (R2) can be derived from (3), (2) and (1).
* result (R3) can be derived from (2) $\alpha$, fine-structure constant formulation given above

### Newtonian Constant of Gravitation (G)

According to Newton's law of universal gravitation, the attractive force (F) between two point-like bodies is directly proportional to the product of their masses (m1 and m2) and inversely proportional to the square of the distance, r, between their centers of mass:

$$F=G{\frac {m_{1}m_{2}}{r^{2}}}$$

(Ref: [Gravitational constant - Wikipedia](https://en.wikipedia.org/wiki/Gravitational_constant))

[Based on the latest measurements of the newtonian gravitational constant](https://physics.nist.gov/cgi-bin/cuu/Value?bg|search_for=newtonian+constant+of+gravitation) the following calculations were done!

#### First Attempt

```shell
> python ./main.py --target-value "6.67430(15)e-11" --target-unit "m^3/(kg s^2)"
```

The program found 4 candidates ([output file](scripts/outputs/analyse_all/newtonian_constant_of_gravitation.txt)) that the resultant unit matched with the target's unit by using the same config file [config/config.json](config/config.json):

```text
	[ M ] [ m³/kg/s² ] = elementary_charge⁴ / (speed_of_light ⋅ planck_constant ⋅ electric_constant² ⋅ electron_mass²)
	  ├── 👎 Not in range.
	  └──  Min (~6✕10⁻¹⁶) < Max (~7✕10⁻⁶) < M̲ ̲(̲~̲5̲✕̲1̲0̲³̲¹̲)̲ 

	[ M ] [ m³/kg/s² ] = elementary_charge² / (electric_constant ⋅ electron_mass²)
	  ├── 👎 Not in range.
	  └──  Min (~6✕10⁻¹⁶) < Max (~7✕10⁻⁶) < M̲ ̲(̲~̲3̲✕̲1̲0̲³̲³̲)̲ 

	[ M ] [ m³/kg/s² ] = speed_of_light ⋅ planck_constant / electron_mass²
	  ├── 👎 Not in range.
	  └──  Min (~6✕10⁻¹⁶) < Max (~7✕10⁻⁶) < M̲ ̲(̲~̲2̲✕̲1̲0̲³̲⁵̲)̲ 

	[ M ] [ m³/kg/s² ] = speed_of_light² ⋅ planck_constant² ⋅ electric_constant / (elementary_charge² ⋅ electron_mass²)
	  ├── 👎 Not in range.
	  └──  Min (~6✕10⁻¹⁶) < Max (~7✕10⁻⁶) < M̲ ̲(̲~̲2̲✕̲1̲0̲³̲⁷̲)̲ 
```

Unfortunately, there are no candidates in the mathematical range for the given scope ([config/config.json](config/config.json)).
We need to add a big dimensionless constant(s) into our mathematical constants scope to place the "M" value in the range.
One of the [Dirac's large number](https://en.wikipedia.org/wiki/Dirac_large_numbers_hypothesis) which is the ratio of the electrical to the gravitational forces between a proton and an electron:

$${\frac {e^{2}}{4\pi \epsilon _{0}Gm_{\text{p}}m_{\text{e}}}}\approx 10^{40}$$

was also tried, but no satisfactory result was found!

#### Second Attempt

In this case, $\sqrt{\mu _{0}/\varepsilon _{0}}$ is added into the definition file:

```text
...
mc_to_ec_ratio = magnetic_constant / electric_constant
sqrt_mc_to_ec_ratio = mc_to_ec_ratio ** 0.5
```

And used in this search ([config/config_g.json](config/config_g.json)).

```shell
> python ./main.py --target-value "6.67430(15)e-11" \
                   --target-unit "m^3/(kg s^2)" \
                   --config-path "./config/config_g.json" \
                   > ./scripts/outputs/analyse_all/newtonian_constant_of_gravitation_with_results.txt
```

The program found 6 candidates ([output file](scripts/outputs/analyse_all/newtonian_constant_of_gravitation_with_results.txt)) that the resultant unit matched with the target's unit and placed on the mathematical range:

```text
	[ M1 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge⁸ ⋅ mc_to_ec_ratio² / (planck_constant³ ⋅ electron_mass²)
	[ M2 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge⁶ ⋅ sqrt_mc_to_ec_ratio³ / (planck_constant² ⋅ electron_mass²)
	[ M3 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge⁴ ⋅ mc_to_ec_ratio / (planck_constant ⋅ electron_mass²)
	[ M4 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge² ⋅ sqrt_mc_to_ec_ratio / electron_mass²
	[ M5 ] [ m³/kg/s² ] = speed_of_light ⋅ planck_constant / electron_mass²
	[ M6 ] [ m³/kg/s² ] = speed_of_light ⋅ planck_constant² / (elementary_charge² ⋅ electron_mass² ⋅ sqrt_mc_to_ec_ratio)
```

And these are the matched results for the given scope:

```text
Result(s) matched the target:
	(6.67430 ± 0.00015)✕10⁻¹¹ m³/kg/s²
R1)	 6.67422✕10⁻¹¹ m³/kg/s² ≈ fine_structure_constant² ⋅ speed_of_light ⋅ elementary_charge⁸ ⋅ mc_to_ec_ratio² / (3 ⋅ 5³ ⋅ pi⁴ ⋅ proton_to_electron_mass_ratio⁹ ⋅ planck_constant³ ⋅ electron_mass²)
R2)	 6.67422✕10⁻¹¹ m³/kg/s² ≈ 2 ⋅ fine_structure_constant³ ⋅ speed_of_light ⋅ elementary_charge⁶ ⋅ sqrt_mc_to_ec_ratio³ / (3 ⋅ 5³ ⋅ pi⁴ ⋅ proton_to_electron_mass_ratio⁹ ⋅ planck_constant² ⋅ electron_mass²)
R3)	 6.67422✕10⁻¹¹ m³/kg/s² ≈ 2² ⋅ fine_structure_constant⁴ ⋅ speed_of_light ⋅ elementary_charge⁴ ⋅ mc_to_ec_ratio / (3 ⋅ 5³ ⋅ pi⁴ ⋅ proton_to_electron_mass_ratio⁹ ⋅ planck_constant ⋅ electron_mass²)
```

If you look at the all candidates list on the above, there is a pattern between sequential results:

```text
G = M1 ⋅ speed_of_light ⋅ elementary_charge⁸ ⋅ mc_to_ec_ratio² / (planck_constant³ ⋅ electron_mass²)
G = M2 ⋅ speed_of_light ⋅ elementary_charge⁶ ⋅ sqrt_mc_to_ec_ratio³ / (planck_constant² ⋅ electron_mass²)
G = M3 ⋅ speed_of_light ⋅ elementary_charge⁴ ⋅ mc_to_ec_ratio / (planck_constant ⋅ electron_mass²)
...
```

Let's look at the ratio of sequential candidates by taking the M(n) values from the latest results:

```text
1 = (M(n) / M(n+1)) ⋅ elementary_charge² ⋅ sqrt_mc_to_ec_ratio / planck_constant
1 = (1 / (2 ⋅ fine_structure_constant)) ⋅ elementary_charge² ⋅ sqrt_mc_to_ec_ratio / planck_constant
1 = 1
```

It means that, the program actually found a single candidate not 6 different one. Let's formulate one of it for example (R3):

$$ G \approx {\frac {2^{2}}{3\cdot5^{3}\cdot\pi^{4}}}\cdot{\frac {\alpha^{4} \,e^{4} \,c\,\mu _{0}}{h\,\varepsilon _{0}}\cdot{\frac {\\m_{e}^{7}}{\\m_{p}^{9}}}} $$

* $\alpha$ is the fine-structure constant
* $h$ is the planck constant
* $c$ is the speed of light in vacuum
* $e$ is the elementary charge
* $\\m_{e}$ is the mass of a stationary electron
* $\\m_{p}$ is the mass of proton
* $\mu _{0}$ is the vacuum permeability (magnetic constant)
* $\varepsilon _{0}$ is the vacuum permittivity (electric constant)
* $\pi$ is the ratio of a circle's circumference to its diameter (mathematical constant)

I am sure that this equation can be re-formed in various ways. It can also be formed by using Rydberg constant as well.
But I think the followings are import:

* The results are only gathered from numeric experiments. If you increase the mathematical scope (especially having less significant digit in target like here) you may get totally different results.
* On building the config files:
  * Tried to increase physical dimensional scope by adding meaningful combinations
  * In mathematical constants, it is tried to use as much as possible those that were placed on existing physical formulas.
* Lastly, these results are wrong until it is proven!

I hope the approach and the results make sense to physicists on helping the understanding of the mystery of the universe!

## Tests

Test folder is [src/tests](src/tests). To run the all test:

```shell
> pytest
```

## Resources

### Libraries & Documentation

* [pint](https://pint.readthedocs.io/en/stable/)
  * [pint repository](https://github.com/hgrecco/pint/tree/master/pint)
  * [pint default constants definition file](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt)
  * [pint developer reference](https://pint.readthedocs.io/en/stable/developers_reference.html)
  * [pint tutorıal](https://pint.readthedocs.io/en/stable/tutorial.html)
* [decimal](https://docs.python.org/3/library/decimal.html)
* [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
  * To validate config file
* [Latex Mathematics](https://en.wikibooks.org/wiki/LaTeX/Mathematics)
  * [Writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)

### Physical Constants

* [The NIST Reference on Constants, Units, and Uncertainty (CODATA 2018 values)](https://physics.nist.gov/cuu/Constants/index.html)
* [NIST, Fundamental Physical Constants — Extensive Listing](https://physics.nist.gov/cuu/pdf/all.pdf)

## Future Work

* For found results, display the previous and next mathematical values to understand how accurately the numerical values to the right of the equation fall within the target error range.
* Investigate possibility of finding all (known) physical constants with a single config file? Targeting `1.0000` with `dimensionless`, methodology can be usefully for this purpose, like:

```shell
> python ./main.py --target-value "1.00000E+0" --target-unit ""
```

* Calculate error value on multiplications and show it on the result. To achieve that, define error values in the definition file. [uncertainties library](https://uncertainties-python-package.readthedocs.io/en/latest/) can be a good candidate!
* Store mathematical calculation results to a file to speed up calculations.
* Store results into the output file. Currently, results are printed to the console.
* Use python [logging](https://docs.python.org/3/howto/logging.html) instead of `print`.

## Gratitude

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

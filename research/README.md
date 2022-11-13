# Researches

This work contains exploration of some well-known physical constants and experiments for some unknown constants by using the `physics-constant-explorer` program explained on the [root folder](..).

## Table of Content

<!-- TOC -->
* [Exploring Derived Physical Constants](#exploring-derived-physical-constants)
  * [Stefan–Boltzmann Constant](#stefanboltzmann-constant)
  * [Rydberg Constant](#rydberg-constant)
  * [Fine Structure Constant](#fine-structure-constant)
  * [Molar Gas Constant](#molar-gas-constant)
  * [Vacuum Permeability (Magnetic Constant)](#vacuum-permeability--magnetic-constant-)
  * [Wien Frequency Displacement Law Constant](#wien-frequency-displacement-law-constant)
  * [Impedance of Free Space](#impedance-of-free-space)
  * [Josephson Constant](#josephson-constant)
  * [Von Klitzing Constant](#von-klitzing-constant)
* [Exploring Planck Units](#exploring-planck-units)
  * [Planck Length](#planck-length)
  * [Planck Mass](#planck-mass)
  * [Planck Time](#planck-time)
  * [Planck Temperature](#planck-temperature)
* [Exploring Some Physics Problem](#exploring-some-physics-problem)
  * [Tides](#tides)
  * [Black Hole Density](#black-hole-density)
* [Experiments](#experiments)
  * [Magnetic Constant to Electric Constant Ratio](#magnetic-constant-to-electric-constant-ratio)
    * [Introduction](#introduction)
      * [Speed of Light in Vacuum (1)](#speed-of-light-in-vacuum--1-)
      * [Fine-structure Constant (2)](#fine-structure-constant--2-)
      * [Rydberg Constant (3)](#rydberg-constant--3-)
    * [Results](#results)
  * [Newtonian Constant of Gravitation](#newtonian-constant-of-gravitation)
    * [Newtonian Constant of Gravitation - Attempt 01](#newtonian-constant-of-gravitation---attempt-01)
      * [Results](#results)
    * [Newtonian Constant of Gravitation - Attempt 02](#newtonian-constant-of-gravitation---attempt-02)
      * [Introduction](#introduction)
      * [Results](#results)
* [Resources](#resources)
  * [Libraries & Documentation](#libraries--documentation)
  * [Physical Constants](#physical-constants)
* [Notes](#notes)
<!-- TOC -->

## Exploring Derived Physical Constants

The script ([derived_constants.sh](script/derived_constants.sh)) is prepared to explore all derived physical constants listed on this section.

The script was executed on the project root folder, and it stored the results referenced in this section:

```shell
> research/script/derived_constants.sh
```

The same default config file ([default_config.json](../src/resources/default_config.json)) is used on the calculations.

### Stefan–Boltzmann Constant

The formulation of Stefan–Boltzmann Constant in terms of other fundamental physical constants:

```math
\sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}} \approxeq 5.670374\times 10^{-8}\,\mathrm{kg}\,\mathrm{s}^{-3}\,\mathrm{K}^{-4}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?sigma|search_for=stefan) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "5.670374419E-8" --target-unit "kg/(s^3 K^4)"
...
Result(s) matched the target:
	(5.6703744195 ± 0.0000000005)✕10⁻⁸ kg/K⁴/s³
	 5.6703744192✕10⁻⁸ kg/K⁴/s³ ≈ 2 ⋅ pi⁵ ⋅ boltzmann_constant⁴ / (3 ⋅ 5 ⋅ speed_of_light² ⋅ planck_constant³)
```

You can examine the output file ([output/derived_constants/stefan_boltzmann_constant.txt](output/derived_constants/stefan_boltzmann_constant.txt)) in detail from this link.

### Rydberg Constant

The formulation of Rydberg Constant in terms of other fundamental physical constants:

```math
R_{\infty }={\frac {m_{\text{e}}e^{4}}{8\varepsilon _{0}^{2}h^{3}c}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Rydberg_constant) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?ryd|search_for=rydberg+constant) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m"
...
Result(s) matched the target:
	(1.0973731568160 ± 0.0000000000021)✕10⁷ 1/m
	 1.0973731568160✕10⁷ 1/m ≈ elementary_charge⁴ ⋅ electron_mass / (2³ ⋅ speed_of_light ⋅ planck_constant³ ⋅ electric_constant²)
```

You can examine the output file ([output/derived_constants/rydberg_constant.txt](output/derived_constants/rydberg_constant.txt)) in detail from this link.

### Fine Structure Constant

The formulation of Fine Structure Constant in terms of other fundamental physical constants:

```math
\alpha ={\frac {e^{2}}{2\varepsilon _{0}hc}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Fine-structure_constant) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?alph|search_for=fine+structure+constant) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "7.2973525693(11)E-3" --target-unit ""
...
Result(s) matched the target:
	(7.2973525693 ± 0.0000000011)✕10⁻³ dimensionless
	 7.2973525693✕10⁻³  ≈ elementary_charge² / (2 ⋅ speed_of_light ⋅ planck_constant ⋅ electric_constant)
```

You can examine the output file ([output/derived_constants/fine_structure_constant.txt](output/derived_constants/fine_structure_constant.txt)) in detail from this link.

### Molar Gas Constant

The formulation of Molar Gas Constant in terms of other fundamental physical constants:

```math
R=N_{\rm {A}}k_{\rm {B}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Gas_constant) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?r|search_for=molar+gas+constant) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "8.314462618E0" --target-unit "(kg m^2)/(K mol s^2)"
...
Result(s) matched the target:
	(8.3144626185 ± 0.0000000005) kg·m²/K/mol/s²
	 8.3144626182✕10⁰ kg·m²/K/mol/s² ≈ boltzmann_constant ⋅ avogadro_constant
```

You can examine the output file ([output/derived_constants/molar_gas_constant.txt](output/derived_constants/molar_gas_constant.txt)) in detail from this link.

### Vacuum Permeability (Magnetic Constant)

The formulation of Vacuum Permeability (Magnetic Constant) in terms of other fundamental physical constants:

```math
\mu _{0}={1 \over {c^{2}\varepsilon _{0}}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Vacuum_permeability) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?mu0|search_for=vacuum+permeability) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "1.25663706212(19)e-6" --target-unit "m kg/(A^2 s^2)"
...
Result(s) matched the target:
	(1.25663706212 ± 0.00000000019)✕10⁻⁶ kg·m/A²/s²
	 1.25663706213✕10⁻⁶ kg·m/A²/s² ≈ 1 / (speed_of_light² ⋅ electric_constant)
```

You can examine the output file ([output/derived_constants/magnetic_constant.txt](output/derived_constants/magnetic_constant.txt)) in detail from this link.

### Wien Frequency Displacement Law Constant

The formulation of Wien Frequency Displacement Law Constant in terms of other fundamental physical constants:

```math
\nu _{\text{peak}}={\alpha  \over h}kT\approx (5.879\times 10^{10}\ \mathrm {Hz/K} )\cdot T
```

You can find [detailed information](https://en.wikipedia.org/wiki/Wien%27s_displacement_law#Frequency-dependent_formulation) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?bpwien|search_for=wien_frequency+displacement+law+constant) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "5.878925757E+10" --target-unit "1/(K s)"
...
Result(s) matched the target:
	(5.8789257575 ± 0.0000000005)✕10¹⁰ 1/K/s
	 5.8789257576✕10¹⁰ 1/K/s ≈ wien_u ⋅ boltzmann_constant / planck_constant
```

You can examine the output file ([output/derived_constants/wien_frequency_displacement_law_constant.txt](output/derived_constants/wien_frequency_displacement_law_constant.txt)) in detail from this link.

### Impedance of Free Space

The formulation of Impedance of Free Space in terms of other fundamental physical constants:

```math
Z_{0}={\frac {E}{H}}=\mu _{0}c={\sqrt {\frac {\mu _{0}}{\varepsilon _{0}}}}={\frac {1}{\varepsilon _{0}c}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Impedance_of_free_space#Relation_to_other_constants) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?z0|search_for=characteristic+impedance+of+vacuum) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "3.76730313668(57)E+2" --target-unit "(kg m^2)/(s^3 A^2)"
...
Result(s) matched the target:
	(3.76730313668 ± 0.00000000057)✕10² kg·m²/A²/s³
	 3.76730313668✕10² kg·m²/A²/s³ ≈ 1 / (speed_of_light ⋅ electric_constant)
```

You can examine the output file ([output/derived_constants/impedance_of_free_space.txt](output/derived_constants/impedance_of_free_space.txt)) in detail from this link.

### Josephson Constant

The formulation of Josephson Constant in terms of other fundamental physical constants:

```math
1 / \Phi _{B}={\frac {2e}{h}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Magnetic_flux_quantum) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?kjos|search_for=josephson) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "4.835978484E+14" --target-unit "(A s^2)/(kg m^2)"
...
Result(s) matched the target:
	(4.8359784845 ± 0.0000000005)✕10¹⁴ A·s²/kg/m²
	 4.8359784842✕10¹⁴ A·s²/kg/m² ≈ 2 ⋅ elementary_charge / planck_constant
```

You can examine the output file ([output/derived_constants/josephson_constant.txt](output/derived_constants/josephson_constant.txt)) in detail from this link.

### Von Klitzing Constant

The formulation of Von Klitzing Constant in terms of other fundamental physical constants:

```math
\R _{K}={\frac {h}{e^{2}}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Quantum_Hall_effect#Applications) about this constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?rk|search_for=von+Klitzing+constant) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "2.581280745E+4" --target-unit "(kg m^2)/(A^2 s^3)"
...
Result(s) matched the target:
	(2.5812807455 ± 0.0000000005)✕10⁴ kg·m²/A²/s³
	 2.5812807459✕10⁴ kg·m²/A²/s³ ≈ planck_constant / elementary_charge²
```

You can examine the output file ([output/derived_constants/von_klitzing_constant.txt](output/derived_constants/von_klitzing_constant.txt)) in detail from this link.

## Exploring Planck Units

Planck considered only the units based on the universal constants $\displaystyle G$, $\displaystyle h$,
$\displaystyle c$, and $\displaystyle k_{\rm B}$ to arrive at natural units for length, time, mass, and temperature.
His definitions differ from the modern ones by a factor of $\displaystyle {\sqrt {2\pi }}$,
because the modern definitions use $\displaystyle \hbar$  rather than $\displaystyle h$.
([Planck units - Wikipedia](https://en.wikipedia.org/wiki/Planck_units#History_and_definition))

The script ([planck_units.sh](script/planck_units.sh)) is prepared to explore the Planck Units listed on this section.

The script was executed on the project root folder, and it stored the results referenced in this section:

```shell
> research/script/planck_units.sh
```

The same config file ([planck_units.json](config/planck_units/plank_units.json)) is used on the calculations.

### Planck Length

The definition of Planck Length:

```math
l_{\text{P}}={\sqrt {\frac {\hbar G}{c^{3}}}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Planck_units#History_and_definition) about this planck constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?plkl|search_for=Planck+length) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "1.616255(18)E-35" \
                   --target-unit "m" \
                   --config-file "research/config/planck_units/plank_units.json" \
                   --definition-file "research/definition/default_en.txt"
...
Result(s) matched the target:
	(1.616255 ± 0.000018)✕10⁻³⁵ m
	 1.616255✕10⁻³⁵ m ≈ sqrt_planck_constant ⋅ sqrt_newtonian_constant_of_gravitation / (sqrt_2 ⋅ sqrt_pi ⋅ sqrt_speed_of_light³)
```

You can examine the output file ([output/planck_units/planck_length.txt](output/planck_units/planck_length.txt)) in detail from this link.

### Planck Mass

The definition of Planck Mass:

```math
m_{\text{P}}={\sqrt {\frac {\hbar c}{G}}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Planck_units#History_and_definition) about this planck constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?plkm|search_for=Planck+mass) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "2.176434(24)E-8" \
                   --target-unit "kg" \
                   --config-file "research/config/planck_units/plank_units.json" \
                   --definition-file "research/definition/default_en.txt"
...
Result(s) matched the target:
	(2.176434 ± 0.000024)✕10⁻⁸ kg
	 2.176434✕10⁻⁸ kg ≈ sqrt_speed_of_light ⋅ sqrt_planck_constant / (sqrt_2 ⋅ sqrt_pi ⋅ sqrt_newtonian_constant_of_gravitation)
```

You can examine the output file ([output/planck_units/planck_mass.txt](output/planck_units/planck_mass.txt)) in detail from this link.

### Planck Time

The definition of Planck Time:

```math
{\displaystyle t_{\text{P}}={\sqrt {\frac {\hbar G}{c^{5}}}}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Planck_units#History_and_definition) about this planck constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?plkt|search_for=planck+time) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "5.391247(60)E-44" \
                   --target-unit "s" \
                   --config-file "research/config/planck_units/plank_units.json" \
                   --definition-file "research/definition/default_en.txt"
...
Result(s) matched the target:
	(5.391247 ± 0.000060)✕10⁻⁴⁴ s
	 5.391246✕10⁻⁴⁴ s ≈ sqrt_planck_constant ⋅ sqrt_newtonian_constant_of_gravitation / (sqrt_2 ⋅ sqrt_pi ⋅ sqrt_speed_of_light⁵)
```

You can examine the output file ([output/planck_units/planck_time.txt](output/planck_units/planck_time.txt)) in detail from this link.

### Planck Temperature

The definition of Planck Temperature:

```math
{\displaystyle T_{\text{P}}={\sqrt {\frac {\hbar c^{5}}{Gk_{\text{B}}^{2}}}}}
```

You can find [detailed information](https://en.wikipedia.org/wiki/Planck_units#History_and_definition) about this planck constant on Wikipedia.

When we take [the CODATA value of this constant](https://physics.nist.gov/cgi-bin/cuu/Value?plktmp|search_for=planck+temperature) as the target, the program finds the same formula as:

```shell
> python ./main.py --target-value "1.416784(16)E+32" \
                   --target-unit "K" \
                   --config-file "research/config/planck_units/plank_units.json" \
                   --definition-file "research/definition/default_en.txt"
...
Result(s) matched the target:
	(1.416784 ± 0.000016)✕10³² K
	 1.416784✕10³² K ≈ sqrt_speed_of_light⁵ ⋅ sqrt_planck_constant / (sqrt_2 ⋅ sqrt_pi ⋅ sqrt_newtonian_constant_of_gravitation ⋅ boltzmann_constant)
```

You can examine the output file ([output/planck_units/planck_temperature.txt](output/planck_units/planck_temperature.txt)) in detail from this link.

## Exploring Some Physics Problem

### Tides

Tides are the rise and fall of sea levels caused by the combined effects of the gravitational forces exerted by the Moon (and to a much lesser extent, the Sun) and are also caused by the Earth and Moon orbiting one another. (Reference [Wikipedia-Tide](https://en.wikipedia.org/wiki/Tide))
...

### Black Hole Density

...

## Experiments

After executing enough runs on the derived physical constants, it is time to experiment on measured but not theoretically-proofed constants.

Before making the experiments, the default definition file is extended with this [definition](definition/constants_en.txt) file to increase the search space in unit dimensions:

* sqrt_speed_of_light = speed_of_light ** 0.5
* sqrt_planck_constant = planck_constant ** 0.5
* ...

On the results, `sqrt_` prefix was removed for only even powered constants (by dividing the power by 2).

The script "[experiments.sh](script/experiments.sh)" is used on the experiments listed on this section.

Note: Please execute the script on the project's root folder, if you want to test it:

```shell
> ./research/script/experiments.sh
```

### Magnetic Constant to Electric Constant Ratio

Resources related with this experiment:

* [Config file](config/experiments/magnetic_constant_to_electric_constant_ratio.json)
* [Definition file](definition/constants_en.txt)
* [Output file](output/experiments/magnetic_constant_to_electric_constant_ratio.txt)
* [Script file](script/experiments.sh)

#### Introduction

Vacuum Permeability (Magnetic Constant):

* [CODATA value](https://physics.nist.gov/cgi-bin/cuu/Value?mu0|search_for=Vacuum+permeability): $\mu _{0}=1.25663706212(19) \times 10^{-6} \, \mathrm{kg} \, \mathrm{m} \, \mathrm{A}^{-2} \, \mathrm{s}^{-2}$
* [More information](https://en.wikipedia.org/wiki/Vacuum_permeability) on Wikipedia.

Vacuum Permittivity (Electric Constant):

* [CODATA value](https://physics.nist.gov/cgi-bin/cuu/Value?ep0|search_for=Vacuum+permittivity): $\varepsilon _{0}=8.8541878128(13) \times 10^{-12} \,\mathrm{A^{2}}\,\mathrm{s}^{4}\,\mathrm{kg}^{-1}\,\mathrm{m}^{-3}$
* [More information](https://en.wikipedia.org/wiki/Vacuum_permittivity) on Wikipedia.

In the formulation of these following constants alone, there are definitely the same constants placed on the formulation (or in the derived formulation).

* $\mu _{0}$ (magnetic constant)
* $\varepsilon _{0}$ (electric Constant)
* $c$ (speed of light)

So, actually we do not have an independent derivation for $\mu _{0}$, $\varepsilon _{0}$ or $\mu _{0} / \varepsilon _{0}$ ratio itself.

The target of this experiment is exploring the ratio of $\mu _{0} / \varepsilon _{0}$.

We are also expecting the following well-known equations that contain $\varepsilon _{0}$ and $\mu _{0}$ in the results.

##### Speed of Light in Vacuum (1)

c ([speed of light in vacuum](#vacuum-permeability-magnetic-constant)) contains $\varepsilon _{0}$ and $\mu _{0}$:

```math
c={\frac {1}{\sqrt {\varepsilon _{0}\mu _{0}}}}
```

##### Fine-structure Constant (2)

$\alpha$ ([fine-structure constant](#fine-structure-constant)) contains $e$ (elementary charge), $h$ (plank constant), $\varepsilon _{0}$:

```math
\alpha={\frac {e^{2}}{2\varepsilon _{0}hc}}={\frac {e^{2}}{2h}}{\sqrt{\frac {\mu _{0}}{\varepsilon _{0}}}}
```

##### Rydberg Constant (3)

$R_{\infty }$ ([Rydberg constant](#rydberg-constant)) contains $e$, $m_{\text{e}}$ (the rest mass of the electron), $h$ and $c$:

```math
R_{\infty }={\frac {m_{\text{e}}e^{4}}{8\varepsilon _{0}^{2}h^{3}c}}={\frac {m_{\text{e}}e^{4}c}{8h^{3}}}{\frac {\mu _{0}}{\varepsilon _{0}}}
```

#### Results

The target value ($\mu _{0}/\varepsilon _{0}$ ratio) is:

```math
{\frac {\mu _{0}}{\varepsilon _{0}}}=1.4192572923(42) \times 10^{5} \, \mathrm{kg}^{2} \, \mathrm{m}^{4} \, \mathrm{A}^{-4} \, \mathrm{s}^{-6}
```

The error of the target is calculated based on the relative errors.

```text
Totally, unique 4913 mathematical multiplications are calculated & cached!
Found 3 candidates the resultant unit matched with the target's unit:
	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = sqrt_planck_constant⁵ ⋅ sqrt_rydberg_constant / (sqrt_speed_of_light ⋅ elementary_charge⁴ ⋅ sqrt_electron_mass)
	  ├── 👍 In range!
	  └──  Min (~3✕10⁻⁷) < M̲ ̲(̲~̲3̲✕̲1̲0̲⁶̲)̲ < Max (~8✕10¹⁶) 

	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = planck_constant² / elementary_charge⁴
	  ├── 👍 In range!
	  └──  Min (~3✕10⁻⁷) < M̲ ̲(̲~̲7̲✕̲1̲0̲⁸̲)̲ < Max (~8✕10¹⁶) 

	[ M ] [ kg²·m⁴/A⁴/s⁶ ] = sqrt_speed_of_light ⋅ sqrt_planck_constant³ ⋅ sqrt_electron_mass / (elementary_charge⁴ ⋅ sqrt_rydberg_constant)
	  ├── 👍 In range!
	  └──  Min (~3✕10⁻⁷) < M̲ ̲(̲~̲1̲✕̲1̲0̲¹̲¹̲)̲ < Max (~8✕10¹⁶) 
```

And 3 of these numerically matched the target value:

```text
Result(s) matched the target:
	(1.4192572923 ± 0.0000000042)✕10⁵ kg²·m⁴/A⁴/s⁶
R1)	 1.4192572924✕10⁵ kg²·m⁴/A⁴/s⁶ ≈ sqrt_2⁵ ⋅ fine_structure_constant ⋅ sqrt_planck_constant⁵ ⋅ sqrt_rydberg_constant / (sqrt_speed_of_light ⋅ elementary_charge⁴ ⋅ sqrt_electron_mass)
R2)	 1.4192572924✕10⁵ kg²·m⁴/A⁴/s⁶ ≈ 2² ⋅ fine_structure_constant² ⋅ planck_constant² / elementary_charge⁴
R3)	 1.4192572924✕10⁵ kg²·m⁴/A⁴/s⁶ ≈ sqrt_2³ ⋅ fine_structure_constant³ ⋅ sqrt_speed_of_light ⋅ sqrt_planck_constant³ ⋅ sqrt_electron_mass / (elementary_charge⁴ ⋅ sqrt_rydberg_constant)
```

As it was expected,

* The result (R2) is actually the same equation of [(2) $\alpha$](#fine-structure-constant-2)
* The results (R1) and (R3) can be derived from the equation [(3) $R_{\infty }$](#rydberg-constant-3), (2) and [(1) c - speed of light](#speed-of-light-in-vacuum-1).

With this experiment, we have verified numerically these 3 equations,
but could not find a possible alternative formulation for $\mu _{0}/\varepsilon _{0}$ ratio with the given scope.

### Newtonian Constant of Gravitation

According to Newton's law of universal gravitation, the attractive force (F) between two point-like bodies is
directly proportional to the product of their masses (m1 and m2) and inversely proportional to the square of the distance,
r, between their centers of mass (Ref: [Gravitational constant - Wikipedia](https://en.wikipedia.org/wiki/Gravitational_constant)):

```math
F=G{\frac {m_{1}m_{2}}{r^{2}}}
```

Again, [CODATA](https://physics.nist.gov/cgi-bin/cuu/Value?bg|search_for=newtonian+constant+of+gravitation) value of the newtonian gravitational constant
was used on the following calculations.

#### Newtonian Constant of Gravitation - Attempt 01

Resources related with this experiment:

* [Config file - Default](../src/resources/default_config.json)
* [Definition file - Default](https://github.com/hgrecco/pint/blob/master/pint/constants_en.txt)
* [Output file](output/experiments/newtonian_constant_of_gravitation_attempt_01.txt)
* [Script file](script/experiments.sh)

##### Results

In the first attempt, as a scope, the default config file was used. The same config file was also used on the "Exploring Derived Physical Constants" [section above](#exploring-derived-physical-constants).

The program found 4 candidates that the resultant unit matched with the target's unit:

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

Unfortunately, there are no candidates in the mathematical range for the experimented scope ([default_config.json](../src/resources/default_config.json)).

To place the "M" value in the range, it is needed to add a big dimensionless constant(s) into our mathematical constants or needed to change the set of our physical constants.

One of the [Dirac's large number](https://en.wikipedia.org/wiki/Dirac_large_numbers_hypothesis) which is the ratio of the electrical to the gravitational forces between a proton and an electron:

```math
{\frac {e^{2}}{4\pi \epsilon _{0}Gm_{\text{p}}m_{\text{e}}}}\approx 10^{40}
```

It was also tried, but no satisfactory result was found!

#### Newtonian Constant of Gravitation - Attempt 02

Resources related with this experiment:

* [Config file](config/experiments/newtonian_constant_of_gravitation_attempt_02.json)
* [Definition file](definition/constants_en.txt)
* [Output file](output/experiments/newtonian_constant_of_gravitation_attempt_02.txt)
* [Script file](script/experiments.sh)

##### Introduction

In this case, $\sqrt{\mu _{0}/\varepsilon _{0}}$ definition is added into the definition file:

```text
...
mc_to_ec_ratio = magnetic_constant / electric_constant
sqrt_mc_to_ec_ratio = mc_to_ec_ratio ** 0.5
```

And used in the config file.

##### Results

The program found 6 candidates that the resultant unit matched with the target's unit and __the resultant value in the mathematical range__.
Let's number these values as M1, M2, ...

```text
	[ M1 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge⁸ ⋅ mc_to_ec_ratio² / (planck_constant³ ⋅ electron_mass²)
	[ M2 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge⁶ ⋅ sqrt_mc_to_ec_ratio³ / (planck_constant² ⋅ electron_mass²)
	[ M3 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge⁴ ⋅ mc_to_ec_ratio / (planck_constant ⋅ electron_mass²)
	[ M4 ] [ m³/kg/s² ] = speed_of_light ⋅ elementary_charge² ⋅ sqrt_mc_to_ec_ratio / electron_mass²
	[ M5 ] [ m³/kg/s² ] = speed_of_light ⋅ planck_constant / electron_mass²
	[ M6 ] [ m³/kg/s² ] = speed_of_light ⋅ planck_constant² / (elementary_charge² ⋅ electron_mass² ⋅ sqrt_mc_to_ec_ratio)
```

But there are only 3 of these matched with the target value:

```text
Result(s) matched the target:
	(6.67430 ± 0.00015)✕10⁻¹¹ m³/kg/s²
R1)	 6.67422✕10⁻¹¹ m³/kg/s² ≈ fine_structure_constant² ⋅ speed_of_light ⋅ elementary_charge⁸ ⋅ mc_to_ec_ratio² / (3 ⋅ 5³ ⋅ pi⁴ ⋅ proton_to_electron_mass_ratio⁹ ⋅ planck_constant³ ⋅ electron_mass²)
R2)	 6.67422✕10⁻¹¹ m³/kg/s² ≈ 2 ⋅ fine_structure_constant³ ⋅ speed_of_light ⋅ elementary_charge⁶ ⋅ sqrt_mc_to_ec_ratio³ / (3 ⋅ 5³ ⋅ pi⁴ ⋅ proton_to_electron_mass_ratio⁹ ⋅ planck_constant² ⋅ electron_mass²)
R3)	 6.67422✕10⁻¹¹ m³/kg/s² ≈ 2² ⋅ fine_structure_constant⁴ ⋅ speed_of_light ⋅ elementary_charge⁴ ⋅ mc_to_ec_ratio / (3 ⋅ 5³ ⋅ pi⁴ ⋅ proton_to_electron_mass_ratio⁹ ⋅ planck_constant ⋅ electron_mass²)
```

If you look at the all candidates listed on the above, there is a pattern between sequential results:

```text
M1 ⋅ speed_of_light ⋅ elementary_charge⁸ ⋅ mc_to_ec_ratio² / (planck_constant³ ⋅ electron_mass²)
M2 ⋅ speed_of_light ⋅ elementary_charge⁶ ⋅ sqrt_mc_to_ec_ratio³ / (planck_constant² ⋅ electron_mass²)
M3 ⋅ speed_of_light ⋅ elementary_charge⁴ ⋅ mc_to_ec_ratio / (planck_constant ⋅ electron_mass²)
...
```

Let's look at the "ratio" of sequential candidates:

```text
ratio = [M(n) / M(n+1)] ⋅ [elementary_charge² ⋅ sqrt_mc_to_ec_ratio / planck_constant]
ratio = [1 / (2 ⋅ fine_structure_constant))] ⋅ [2 ⋅ fine_structure_constant]
ratio = 1
```

It means that, the program actually found a single candidate not 6 different one. If we write for example (R3) with well-known symbols of the constants:

```math
6.67422✕10⁻¹¹ m³/kg/s² \approx {\frac {2^{2}}{3\cdot5^{3}\cdot\pi^{4}}}\cdot{\frac {\alpha^{4} \,e^{4} \,c\,\mu _{0}}{h\,\varepsilon _{0}}\cdot{\frac {\\m _{e}^{7}}{\\m _{p}^{9}}}}
```

* $\alpha$ is the fine-structure constant
* $h$ is the planck constant
* $c$ is the speed of light in vacuum
* $e$ is the elementary charge
* $\\m _{e}$ is the mass of a stationary electron
* $\\m _{p}$ is the mass of proton
* $\mu _{0}$ is the vacuum permeability (magnetic constant)
* $\varepsilon _{0}$ is the vacuum permittivity (electric constant)
* $\pi$ is the ratio of a circle's circumference to its diameter (mathematical constant)

This equation can be re-formed in various ways.

The followings observations are import while considering and investigating the results found by using this program:

1) If you increase the mathematical constants scope (especially having less significant digit targets, such as `G` here, it only has 6 significant digits) you may get different results.
2) It is better to select mathematical constants which were used on previous explorations.

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

## Notes

The results found on this research are only numerical and not a physical proof!

I hope the approach and the results make sense to physicists in helping the understanding of the mystery of the universe!

TEST

print(f"v:L~ {v:L~}")

```math
\frac{\mathrm{c} \cdot \mathrm{e}^{2} \cdot \mathrm{ℎ}}{\left(\mathrm{N\_A} \cdot \mathrm{k} \cdot \mathrm{m\_e} \cdot \mathrm{µ\_0} \cdot \mathrm{ε\_0}\right)}
```

print(f"v:Lx~ {v:Lx~}")

```math
\SI[]{10}{\elementary_charge\tothe{2.000}\planck_constant\speed_of_light\per\avogadro_constant\per\boltzmann_constant\per\electron_mass\per\vacuum_permeability\per\vacuum_permittivity}
```

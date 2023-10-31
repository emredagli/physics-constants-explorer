# Researches

This work contains exploration of some well-known physical constants and experiments for 
some unknown constants by using the `physics-constant-explorer` program explained on the [repo home page](../README.md).

## Table of Content

<!-- TOC -->
* [1 Exploring Derived Physical Constants](#1-exploring-derived-physical-constants)
* [2 Exploring Planck Units](#2-exploring-planck-units)
* [3 Experiments](#3-experiments)
  * [3.1 Magnetic Constant to Electric Constant Ratio](#31-magnetic-constant-to-electric-constant-ratio)
  * [3.2 Newtonian Constant of Gravitation](#32-newtonian-constant-of-gravitation)
* [4 Resources](#4-resources)
  * [4.1 Physical Constants](#41-physical-constants)
* [5 Acknowledgement & Gratitude](#5-acknowledgement--gratitude)
* [6 Final Notes](#6-final-notes)
<!-- TOC -->

## 1 Exploring Derived Physical Constants

The script ([derived_constants.sh](script/derived_constants.sh)) is prepared to explore some constants that can be derived in terms of fundamental constants.

* The default config file ([default_config.json](../src/resources/default_config.json)) was used on all calculations!
* The default definition file ([default_definition.json](../src/resources/default_definition.json)) was used.
* CODATA values were used as target numeric values.

The script was executed on the project root folder, and it stored the results given on the table below:
```shell
> research/script/derived_constants.sh
```

| Constant Name                                                                                                                                              | Derivation                                                                                          | The Program Input<br>[CODATA](https://physics.nist.gov/cuu/Constants/) Constant Values                           | The Results                                                        | Stored Output                                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Stefan–Boltzmann Constant](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant)                                                               | $$\sigma ={\frac {2\pi ^{5}k^{4}}{15c^{2}h^{3}}}$$                                                  | {&nbsp;[5.670374419E-8](https://physics.nist.gov/cgi-bin/cuu/Value?sigma)&nbsp;}<br>[&nbsp;kg/K⁴/s³&nbsp;]       | (2⋅π⁵&nbsp;/&nbsp;(3⋅5))&nbsp;⋅&nbsp;(k⁴&nbsp;/&nbsp;(h³⋅c²))      | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/stefan_boltzmann_constant.txt)                |
| [Rydberg Constant](https://en.wikipedia.org/wiki/Rydberg_constant)                                                                                         | $$R_{\infty }={\frac {m_{\text{e}}e^{4}}{8\varepsilon _{0}^{2}h^{3}c}}$$                            | {&nbsp;[1.0973731568160(21)e+7](https://physics.nist.gov/cgi-bin/cuu/Value?ryd)&nbsp;}<br>[&nbsp;1/m&nbsp;]      | 1&nbsp;/&nbsp;2³&nbsp;⋅&nbsp;(m_e⋅e⁴&nbsp;/&nbsp;(h³⋅c⋅ε_0²))      | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/rydberg_constant.txt)                         |
| [Fine Structure Constant](https://en.wikipedia.org/wiki/Fine-structure_constant)                                                                           | $$\alpha ={\frac {e^{2}}{2\varepsilon _{0}hc}}$$                                                    | {&nbsp;[7.2973525693(11)E-3](https://physics.nist.gov/cgi-bin/cuu/Value?alph)&nbsp;}<br>[&nbsp;-&nbsp;]          | 1&nbsp;/&nbsp;2&nbsp;⋅&nbsp;(e²&nbsp;/&nbsp;(h⋅c⋅ε_0))             | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/fine_structure_constant.txt)                  |
| [Molar Gas Constant](https://en.wikipedia.org/wiki/Gas_constant)                                                                                           | $$R=N_{\rm {A}}k_{\rm {B}}$$                                                                        | {&nbsp;[8.314462618E0](https://physics.nist.gov/cgi-bin/cuu/Value?r)&nbsp;}<br>[&nbsp;kg·m²/K/mol/s²&nbsp;]      | N_A⋅k                                                              | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/molar_gas_constant.txt)                       |
| [Vacuum Magnetic Permeability](https://en.wikipedia.org/wiki/Vacuum_permeability)                                                                          | $$\mu _{0}={1 \over {c^{2}\varepsilon _{0}}}$$                                                      | {&nbsp;[1.25663706212(19)e-6](https://physics.nist.gov/cgi-bin/cuu/Value?mu0)&nbsp;}<br>[&nbsp;kg·m/A²/s²&nbsp;] | 1&nbsp;/&nbsp;(c²⋅ε_0)                                             | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/vacuum_magnetic_permeability.txt)             |
| [Wien's Displacement Law](https://en.wikipedia.org/wiki/Wien%27s_displacement_law#Frequency-dependent_formulation)                                         | $$\nu _{\text{peak}}={\alpha  \over h}kT$$                                                          | {&nbsp;[5.878925757E+10](https://physics.nist.gov/cgi-bin/cuu/Value?bpwien)&nbsp;}<br>[&nbsp;1/K/s&nbsp;]        | w_u&nbsp;⋅&nbsp;(k&nbsp;/&nbsp;h)                                  | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/wien_frequency_displacement_law_constant.txt) |
| [Impedance of Free Space](https://en.wikipedia.org/wiki/Impedance_of_free_space#Relation_to_other_constants)                                               | $$Z_{0}={\frac {1}{\varepsilon _{0}c}}$$                                                            | {&nbsp;[3.76730313668(57)E+2](https://physics.nist.gov/cgi-bin/cuu/Value?z0)&nbsp;}<br>[&nbsp;kg·m²/A²/s³&nbsp;] | 1&nbsp;/&nbsp;(c⋅ε_0)                                              | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/impedance_of_free_space.txt)                  |
| [Josephson Constant](https://en.wikipedia.org/wiki/Magnetic_flux_quantum)                                                                                  | $$1 / \Phi _{B}={\frac {2e}{h}}$$                                                                   | {&nbsp;[4.835978484E+14](https://physics.nist.gov/cgi-bin/cuu/Value?kjos)&nbsp;}<br>[&nbsp;A·s²/kg/m²&nbsp;]     | 2&nbsp;⋅&nbsp;(e&nbsp;/&nbsp;h)                                    | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/josephson_constant.txt)                       |
| [Von Klitzing Constant](https://en.wikipedia.org/wiki/Quantum_Hall_effect#Applications)                                                                    | $$\mathrm{R} _{K}={\frac {h}{e^{2}}} $$                                                             | {&nbsp;[2.581280745E+4](https://physics.nist.gov/cgi-bin/cuu/Value?rk)&nbsp;}<br>[&nbsp;kg·m²/A²/s³&nbsp;]       | h&nbsp;/&nbsp;e²                                                   | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/von_klitzing_constant.txt)                    |
| [Bohr Magneton](https://en.wikipedia.org/wiki/Bohr_magneton)                                                                                               | $$\mu _{\mathrm{B}}=\frac{e\hbar}{2m _{\mathrm{e}}}$$                                               | {&nbsp;[9.2740100783(28)E-24](https://physics.nist.gov/cgi-bin/cuu/CCValue?mub)&nbsp;}<br>[&nbsp;A·m²&nbsp;]     | (1&nbsp;/&nbsp;(2²⋅π))&nbsp;⋅&nbsp;(e⋅h&nbsp;/&nbsp;m_e)           | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/bohr_magneton.txt)                            |
| [Nuclear Magneton](https://en.wikipedia.org/wiki/Nuclear_magneton)                                                                                         | $$\mu _{\text{N}}={{e\hbar } \over {2m _{\text{p}}}}$$                                              | {&nbsp;[5.0507837461(15)E-27](https://physics.nist.gov/cgi-bin/cuu/Value?mun)&nbsp;}<br>[&nbsp;A·m²&nbsp;]       | (1&nbsp;/&nbsp;(2²⋅π⋅(m_p/m_e)))&nbsp;⋅&nbsp;(e⋅h&nbsp;/&nbsp;m_e) | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/nuclear_magneton.txt)                         |
| [Proton Gyromagnetic Ratio](https://de.wikipedia.org/wiki/Gyromagnetisches_Verh%C3%A4ltnis#%CE%B3%E2%84%93_f%C3%BCr_reinen_Bahndrehimpuls_eines_Elektrons) | $$\gamma _{\mathrm {p} }={\frac {e}{2m _{\mathrm {p} }}}\cdot g _{\mathrm {p} }$$                   | {&nbsp;[2.6752218744(11)E+8](https://physics.nist.gov/cgi-bin/cuu/Value?gammap)&nbsp;}<br>[&nbsp;A·s/kg&nbsp;]   | (g_p&nbsp;/&nbsp;(2⋅(m_p/m_e)))&nbsp;⋅&nbsp;(e&nbsp;/&nbsp;m_e)    | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/proton_gyromagnetic_ratio.txt)                |
| [Bohr Radius](https://en.wikipedia.org/wiki/Bohr_radius)                                                                                                   | $$a_{0}={\frac {\varepsilon _{0}h^{2}}{\pi e^{2}m _{\text{e}}}}$$                                   | {&nbsp;[5.29177210903(80)E-11](https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0)&nbsp;}<br>[&nbsp;m&nbsp;]   | 1&nbsp;/&nbsp;π&nbsp;⋅&nbsp;(h²⋅ε_0&nbsp;/&nbsp;(m_e⋅e²))          | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/bohr_radius.txt)                              |
| [Hartree Energy](https://en.wikipedia.org/wiki/Hartree)                                                                                                    | $$E_{\mathrm {h} }=m _{\mathrm {e} }\left({\frac {e^{2}}{4\pi \varepsilon _{0}\hbar }}\right)^{2}$$ | {&nbsp;[4.3597447222071(85)E-18](https://physics.nist.gov/cgi-bin/cuu/Value?hr)&nbsp;}<br>[&nbsp;kg·m²/s²&nbsp;] | 1&nbsp;/&nbsp;2²&nbsp;⋅&nbsp;(m_e⋅e⁴&nbsp;/&nbsp;(h²⋅ε_0²))        | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/hartree_energy.txt)                           |
| [Classical Electron Radius](https://en.wikipedia.org/wiki/Classical_electron_radius)                                                                       | $$r_{\mathrm {e} }={\frac {1}{4\pi}}{\frac {e^{2}}{m_{\text{e}}c^{2} \varepsilon _{0}}}$$           | {&nbsp;[2.8179403262(13)E-15](https://physics.nist.gov/cgi-bin/cuu/Value?re)&nbsp;}<br>[&nbsp;m&nbsp;]           | (1&nbsp;/&nbsp;(2²⋅π))&nbsp;⋅&nbsp;(e²&nbsp;/&nbsp;(m_e⋅c²⋅ε_0))   | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/classical_electron_radius.txt)                |
| [Thomson Cross Section](https://en.wikipedia.org/wiki/Thomson_scattering)                                                                                  | $$\sigma _{t}={\frac {8\pi }{3}}\left({\frac {q^{2}}{4\pi \varepsilon _{0}mc^{2}}}\right)^{2}$$     | {&nbsp;[2.8179403262(13)E-15](https://physics.nist.gov/cgi-bin/cuu/Value?sigmae)&nbsp;}<br>[&nbsp;m&nbsp;]       | (1&nbsp;/&nbsp;(2²⋅π))&nbsp;⋅&nbsp;(e²&nbsp;/&nbsp;(m_e⋅c²⋅ε_0))   | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/derived_constants/classical_electron_radius.txt)                |
| ...                                                                                                                                                        |                                                                                                     |                                                                                                                  |                                                                    |                                                                                                                                                                               |

## 2 Exploring Planck Units

"Planck considered only the units based on the universal constants $\displaystyle G$, $\displaystyle h$, 
$\displaystyle c$, and $\displaystyle k_{\rm B}$ to arrive at natural units for length, time, mass, and temperature.
His definitions differ from the modern ones by a factor of $\displaystyle {\sqrt {2\pi }}$, 
because the modern definitions use $\displaystyle \hbar$  rather than $\displaystyle h$."
([Planck units - Wikipedia](https://en.wikipedia.org/wiki/Planck_units#History_and_definition))

The script ([planck_units.sh](script/planck_units.sh)) is prepared to explore the Planck Units.

* The config file ([planck_units.json](config/planck_units/plank_units.json)) is used on the calculations.
* The default definition file ([default_definition.json](../src/resources/default_definition.json)) is used.
* Again, CODATA values were picked as target numeric values.

The script was executed on the project root folder, and it stored the results given on the table below:
```shell
> research/script/planck_units.sh
```


| Constant Name                                                                           | Derivation                                                                        | The Program Input<br>[CODATA](https://physics.nist.gov/cuu/Constants/) Constant Values                 | The Results                                                              | Stored Output                                                                                                                                      |
|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| [Planck Length](https://en.wikipedia.org/wiki/Planck_units#History_and_definition)      | $$l_{\text{P}}={\sqrt {\frac {\hbar G}{c^{3}}}}$$                                 | {&nbsp;[1.616255(18)E-35](https://physics.nist.gov/cgi-bin/cuu/Value?plkl)&nbsp;}<br>[&nbsp;m&nbsp;]   | (1&nbsp;/&nbsp;(2¹ᐟ²⋅π¹ᐟ²))&nbsp;⋅&nbsp;(G¹ᐟ²⋅h¹ᐟ²&nbsp;/&nbsp;c³ᐟ²)     | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/planck_units/planck_length.txt)      |
| [Planck Mass](https://en.wikipedia.org/wiki/Planck_units#History_and_definition)        | $$m_{\text{P}}={\sqrt {\frac {\hbar c}{G}}}$$                                     | {&nbsp;[2.176434(24)E-8](https://physics.nist.gov/cgi-bin/cuu/Value?plkm)&nbsp;}<br>[&nbsp;kg&nbsp;]   | (1&nbsp;/&nbsp;(2¹ᐟ²⋅π¹ᐟ²))&nbsp;⋅&nbsp;(h¹ᐟ²⋅c¹ᐟ²&nbsp;/&nbsp;G¹ᐟ²)     | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/planck_units/planck_mass.txt)        |
| [Planck Time](https://en.wikipedia.org/wiki/Planck_units#History_and_definition)        | $${\displaystyle t_{\text{P}}={\sqrt {\frac {\hbar G}{c^{5}}}}}$$                 | {&nbsp;[5.391247(60)E-44](https://physics.nist.gov/cgi-bin/cuu/Value?plkt)&nbsp;}<br>[&nbsp;s&nbsp;]   | (1&nbsp;/&nbsp;(2¹ᐟ²⋅π¹ᐟ²))&nbsp;⋅&nbsp;(G¹ᐟ²⋅h¹ᐟ²&nbsp;/&nbsp;c⁵ᐟ²)     | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/planck_units/planck_time.txt)        |
| [Planck Temperature](https://en.wikipedia.org/wiki/Planck_units#History_and_definition) | $${\displaystyle T_{\text{P}}={\sqrt {\frac {\hbar c^{5}}{Gk_{\text{B}}^{2}}}}}$$ | {&nbsp;[1.416784(16)E+32](https://physics.nist.gov/cgi-bin/cuu/Value?plktmp)&nbsp;}<br>[&nbsp;K&nbsp;] | (1&nbsp;/&nbsp;(2¹ᐟ²⋅π¹ᐟ²))&nbsp;⋅&nbsp;(h¹ᐟ²⋅c⁵ᐟ²&nbsp;/&nbsp;(k⋅G¹ᐟ²)) | [The&nbsp;output&nbsp;file](https://github.com/emredagli/physics-constants-explorer/blob/main/research/output/planck_units/planck_temperature.txt) |


## 3 Experiments

After executing enough runs on the other physical constants, it is time to experiment on measured but not theoretically-proofed constants.

The script ([experiments.sh](script/experiments.sh)) was used on the experiments listed on this section.

Note: The script was executed on the project's root folder:

```shell
> ./research/script/experiments.sh
```

### 3.1 Magnetic Constant to Electric Constant Ratio

#### 3.1.1 Resources

* [Config File](config/experiments/magnetic_constant_to_electric_constant_ratio.json), and scope:
```text
dimensional constants:   
    c = { 299792458 } [ m/s ], powers = [-1, -1/2, 0, 1/2, 1]
    h = { 6.62607015e-34 } [ kg·m²/s ], powers = [-3, -5/2, -2, -3/2, -1, -1/2, 0, 1/2, 1, 3/2, 2, 5/2, 3]
    e = { 1.602176634e-19 } [ A·s ], powers = [-4, -7/2, -3, -5/2, -2, -3/2, -1, -1/2, 0, 1/2, 1, 3/2, 2, 5/2, 3, 7/2, 4]
    m_e = { 9.1093837015(28)e-31 } [ kg ], powers = [-1, -1/2, 0, 1/2, 1]
    R_∞ = { 10973731.568160(21) } [ 1/m ], powers = [-1/2, 0, 1/2]
dimensionless constants: 
    2, powers = [-4, -7/2, -3, -5/2, -2, -3/2, -1, -1/2, 0, 1/2, 1, 3/2, 2, 5/2, 3, 7/2, 4]
    π, powers = [-4, -7/2, -3, -5/2, -2, -3/2, -1, -1/2, 0, 1/2, 1, 3/2, 2, 5/2, 3, 7/2, 4]
    α, powers = [-4, -7/2, -3, -5/2, -2, -3/2, -1, -1/2, 0, 1/2, 1, 3/2, 2, 5/2, 3, 7/2, 4]
```
* [Default Definition File](../src/resources/default_definition.json)
* [Output File](output/experiments/magnetic_constant_to_electric_constant_ratio.txt)
* [Script File](script/experiments.sh)

#### 3.1.2 Introduction

[Vacuum Magnetic Permeability (Magnetic Constant)](https://en.wikipedia.org/wiki/Vacuum_permeability):

* [CODATA value](https://physics.nist.gov/cgi-bin/cuu/Value?mu0): $\mu _{0}=1.25663706212(19) \times 10^{-6}$ $\mathrm{kg}\cdot\mathrm{m}\cdot\mathrm{s}^{-2}\cdot\mathrm{A}^{-2}$

[Vacuum Electric Permittivity (Electric Constant)](https://en.wikipedia.org/wiki/Vacuum_permittivity):

* [CODATA value](https://physics.nist.gov/cgi-bin/cuu/Value?ep0): $\varepsilon _{0}=8.8541878128(13) \times 10^{-12}$ $\mathrm{A^{2}}\cdot\mathrm{s}^{4}\cdot\mathrm{kg}^{-1}\cdot\mathrm{m}^{-3}$

In this experiment we would like to explore the ratio $\mu _{0} / \varepsilon _{0}$, it is actually the square of [Impedance of free space](https://en.wikipedia.org/wiki/Impedance_of_free_space#Relation_to_other_constants):

We have the following well-known relations and definitions that contain $\mu _{0}$ and $\varepsilon _{0}$ :

##### 3.1.2.1 Speed of Light in Vacuum (1)

c (speed of light in vacuum) contains the multiplication of $\varepsilon _{0}$ and $\mu _{0}$:

```math
c={\frac {1}{\sqrt {\varepsilon _{0}\mu _{0}}}}
```

##### 3.1.2.2 Fine-structure Constant (2)

$\alpha$ (fine-structure constant) contains the ratio $\mu _{0} / \varepsilon _{0}$:

```math
\alpha={\frac {e^{2}}{2\varepsilon _{0}hc}}={\frac {e^{2}}{2h}}{\sqrt{\frac {\mu _{0}}{\varepsilon _{0}}}}
```

##### 3.1.2.3 Rydberg Constant (3)

$R_{\infty }$ (Rydberg constant) contains the ratio $\mu _{0} / \varepsilon _{0}$:

```math
R_{\infty }={\frac {m_{\text{e}}e^{4}}{8\varepsilon _{0}^{2}h^{3}c}}={\frac {m_{\text{e}}e^{4}c}{8h^{3}}}{\frac {\mu _{0}}{\varepsilon _{0}}}
```

#### 3.1.3 Results

The target is:

```math
{\frac {\mu _{0}}{\varepsilon _{0}}}=1.4192572923(42) \times 10^{5} \, \mathrm{kg}^{2}\cdot\mathrm{m}^{4}\cdot\mathrm{A}^{-4}\cdot\mathrm{s}^{-6}
```

Found 3 candidates the resultant unit matched with the target's unit:

```text
	{ Q } [ kg²·m⁴/A⁴/s⁶ ] = h⁵ᐟ²⋅R_∞¹ᐟ² / (m_e¹ᐟ²⋅e⁴⋅c¹ᐟ²)
	  ├── 👍 In range!
	  └── Min (~3E-7) < Q (~3E+6) < Max (~8E+16) 

	{ Q } [ kg²·m⁴/A⁴/s⁶ ] = h² / e⁴
	  ├── 👍 In range!
	  └── Min (~3E-7) < Q (~7E+8) < Max (~8E+16) 

	{ Q } [ kg²·m⁴/A⁴/s⁶ ] = m_e¹ᐟ²⋅h³ᐟ²⋅c¹ᐟ² / (e⁴⋅R_∞¹ᐟ²)
	  ├── 👍 In range!
	  └── Min (~3E-7) < Q (~1E+11) < Max (~8E+16) 
```

And results that overlap with the target:

```text
	{ 1.4192572923(42) e+5 } [ kg²·m⁴/A⁴/s⁶ ] = Target
R1	{ 1.41925729237(43) e+5 } [ kg²·m⁴/A⁴/s⁶ ] = (2⁵ᐟ²⋅α) ⋅ (h⁵ᐟ²⋅R_∞¹ᐟ² / (m_e¹ᐟ²⋅e⁴⋅c¹ᐟ²))
R2	{ 1.41925729236(43) e+5 } [ kg²·m⁴/A⁴/s⁶ ] = (2²⋅α²) ⋅ (h² / e⁴)
R3	{ 1.41925729236(86) e+5 } [ kg²·m⁴/A⁴/s⁶ ] = (2³ᐟ²⋅α³) ⋅ (m_e¹ᐟ²⋅h³ᐟ²⋅c¹ᐟ² / (e⁴⋅R_∞¹ᐟ²))
```

As it was expected,

* The result (R2) is actually the same equation of $\alpha$ [(2) fine-structure constant](#3122-fine-structure-constant-2)
* The results (R1) and (R3) can be derived from the equation $R_{\infty }$ [(3) Rydberg Constant](#3123-rydberg-constant-3), (2) and c [(1) speed of light](#3121-speed-of-light-in-vacuum-1).

With this experiment, these 3 equations were found as we have expected.
But a possible alternative expressions for $\mu _{0}/\varepsilon _{0}$ ratio could not be found (for the given exploration scope)!

### 3.2 Newtonian Constant of Gravitation

"According to Newton's law of universal gravitation, the attractive force (F) between two point-like bodies is
directly proportional to the product of their masses (m1 and m2) and inversely proportional to the square of the distance,
r, between their centers of mass." (Ref: [Gravitational constant - Wikipedia](https://en.wikipedia.org/wiki/Gravitational_constant)):

```math
F=G{\frac {m_{1}m_{2}}{r^{2}}}
```

Again, [CODATA](https://physics.nist.gov/cgi-bin/cuu/Value?bg) value `6.67430(15) E-11` of the Newtonian gravitational constant
was used on the following explorations.


##### 3.2.1 Resources

* [Config file](config/experiments/newtonian_constant_of_gravitation_attempt_01.json)
* [Default Definition File](../src/resources/default_definition.json)
* [Output file](output/experiments/newtonian_constant_of_gravitation_attempt_01.txt)
* [Script file](script/experiments.sh)

##### 3.2.2 Results

The program found some candidates that the resultant unit matched with the target's unit and __the resultant value in the dimensionless range__.

If you look at the found candidates, there is a pattern between these (the first 2 candidates):
```text
    { Q1 } [ m³/kg/s² ] = e¹² / (m_e²⋅h⁵⋅c⁵⋅ε_0⁶)
    { Q2 } [ m³/kg/s² ] = e¹⁰ / (m_e²⋅h⁴⋅c⁴⋅ε_0⁵)
...

The ratio is:
Q1/Q2 = e² / (c⋅ε_0⋅ℎ)
```
As you see, Q1/Q2 is actually the square root of the [fine-structure constant](#3122-fine-structure-constant-2) which is a dimensionless physical constant. 
So we can state that the program actually found a single candidate that dimensionally matched with the target's unit.

We have the following numerically overlapped expression:
```text
Result(s) that overlap with the target:
	{ 6.67430(15) e-11 } [ m³/kg/s² ] = Target
	{ 6.674224928(14) e-11 } [ m³/kg/s² ] = (1 / (2²⋅3⋅5³⋅π⁴⋅(m_p/m_e)⁹)) ⋅ (e¹² / (m_e²⋅h⁵⋅c⁵⋅ε_0⁶))

Where
* (m_p/m_e): proton electron mass ratio
* m_e: electron mass
* e: elementary charge
* h: planck constant
* c: speed of light in vacuum
* ε_0: vacuum electric permittivity
```

__Note that__, if we increase the scope of the dimensionless constant, 
especially targeting numeric values which have less significant digits (such as here, which has only 6 significant digits) we may get different results.

This result may have come across as numerically by chance. But it's still surprising that we could find the expression by using [this simple scope](config/experiments/newtonian_constant_of_gravitation_attempt_01.json) used in this experiment.

## 4 Resources

### 4.1 Physical Constants

* [The NIST Reference on Constants, Units, and Uncertainty (CODATA 2018 values)](https://physics.nist.gov/cuu/Constants/index.html)
* [NIST, Fundamental Physical Constants — Extensive Listing](https://physics.nist.gov/cuu/pdf/all.pdf)
* [Units and Fundamental Constants in Physics and Chemistry, Subvolume b / Editors: J. Bortfeldt and B. Kramer](https://link.springer.com/book/9783540475316)


## 5 Acknowledgement & Gratitude

I am a software engineer with a background in Scientific Computing & Physics and have over 20 years of experience.
Last 4 years I am mainly working in big data related subjects and domains.

I won the honourable mention award in [IPhO 1996 (XXVII Oslo, Norway)](https://www.ipho-new.org/documentations/#statistics).
In the same year, I decided to study computer engineering. Although more than 20 years have passed, I am pleased to be able to use my physics knowledge to develop such an application.

I would like to express my gratitude to my physics teachers who made me love physics during these years:

* Physics Teacher Rafet Kamer, Physics Olympiads
* Prof. Dr. K. Sinan Bilikmen, METU-Physics
* Prof. Dr. Mehmet Tomak, METU-Physics

And who are not with us:

* Prof. Dr. İbrahim Günal (R.I.P), METU-Physics
* Prof. Dr. Ordal Demokan (R.I.P), METU-Physics
* Physics Teacher Aykut Gümüç (R.I.P), Eskisehir Science High School
* Prof. Dr. Oleg Fedorovich Kabardin (R.I.P), Physics Olympiads

And I would like to thank my friends who was supporting me on this work:

* Dr. İnanç Kanık
* Dr. Serkan Cabi
* Dr. Özgür Sümer
* Atılım Çetin
* Osman Özgür
* Ali Onur Geven

And of course to my beloved wife Ayşen and my dear children Ozan & Doruk!

I would also like to thank all the team who have developed and contributed the [pint library](https://pint.readthedocs.io/en/stable/) 👏

Emre Dagli

## 6 Final Notes

The results found in this research are only numerical explorations, they are not a physical proof or a derivation!

I am not sure if a similar physical constant explorer program has been implemented before. 
If it has been implemented already, I hope this approach gives a new perspective on helping 
us to understand the mystery of nature with good purposes!

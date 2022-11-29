#!/bin/sh

output_folder=research/output/derived_constants

# Stefan Boltzmann constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?sigma
python ./main.py --target-value "5.670374419E-8" --target-unit "kg/(s^3 K^4)" > ./$output_folder/stefan_boltzmann_constant.txt &

# Rydberg constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?ryd
python ./main.py --target-value "1.0973731568160(21)E+7" --target-unit "1/m" > ./$output_folder/rydberg_constant.txt &

# Fine-structure constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?alph
python ./main.py --target-value "7.2973525693(11)E-3" --target-unit "" > ./$output_folder/fine_structure_constant.txt &

# Vacuum magnetic permeability constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?mu0
python ./main.py --target-value "1.25663706212(19)E-6" --target-unit "m kg/(A^2 s^2)" > ./$output_folder/vacuum_magnetic_permeability.txt &

# Molar gas constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?r
python ./main.py --target-value "8.314462618E0" --target-unit "(kg m^2)/(K mol s^2)" > ./$output_folder/molar_gas_constant.txt &

# Wien frequency displacement law constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?bpwien
python ./main.py --target-value "5.878925757E+10" --target-unit "1/(K s)" > ./$output_folder/wien_frequency_displacement_law_constant.txt &

# Impedance of free space. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?z0
python ./main.py --target-value "3.76730313668(57)E+2" --target-unit "(kg m^2)/(s^3 A^2)" > ./$output_folder/impedance_of_free_space.txt &

# Josephson constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?kjos
python ./main.py --target-value "4.835978484E+14" --target-unit "(A s^2)/(kg m^2)" > ./$output_folder/josephson_constant.txt &

# von Klitzing constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?rk
python ./main.py --target-value "2.581280745E+4" --target-unit "(kg m^2)/(A^2 s^3)" > ./$output_folder/von_klitzing_constant.txt &

# Bohr magneton. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?mub
python ./main.py --target-value "9.2740100783(28)E-24" --target-unit "A m^2" > ./$output_folder/bohr_magneton.txt &

# Nuclear magneton. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?mun
python ./main.py --target-value "5.0507837461(15)E-27" --target-unit "A m^2" > ./$output_folder/nuclear_magneton.txt &

# Proton gyromagnetic ratio. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?gammap
python ./main.py --target-value "2.6752218744(11)E+8" --target-unit "A s/kg" > ./$output_folder/proton_gyromagnetic_ratio.txt &

# Electron gyromagnetic ratio. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?gammae
python ./main.py --target-value "1.76085963023(53)E+11" --target-unit "A s/kg" > ./$output_folder/electron_gyromagnetic_ratio.txt &

# Proton magnetic moment. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?mup
python ./main.py --target-value "1.41060679736(60)E-26" --target-unit "A m^2" > ./$output_folder/proton_magnetic_moment.txt &

# Bohr radius. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0
python ./main.py --target-value "5.29177210903(80)E-11" --target-unit "m" > ./$output_folder/bohr_radius.txt &

# Hartree energy. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?hr
python ./main.py --target-value "4.3597447222071(85)E-18" --target-unit "kg m^2/s^2" > ./$output_folder/hartree_energy.txt &

# Compton wavelength. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?ecomwl
python ./main.py --target-value "2.42631023867(73)E-12" --target-unit "m" > ./$output_folder/compton_wavelength.txt &


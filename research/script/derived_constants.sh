#!/bin/sh

output_folder=research/output/derived_constants

# Stefan Boltzmann constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?sigma
python ./main.py --target-value "5.670374419E-8" --target-unit "kg/(s^3 K^4)" > ./$output_folder/stefan_boltzmann_constant.txt &

# Rydberg constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?ryd
python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m" > ./$output_folder/rydberg_constant.txt &

# Fine-structure constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?alph
python ./main.py --target-value "7.2973525693(11)E-3" --target-unit "" > ./$output_folder/fine_structure_constant.txt &

# Vacuum magnetic permeability constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?mu0
python ./main.py --target-value "1.25663706212(19)e-6" --target-unit "m kg/(A^2 s^2)" > ./$output_folder/vacuum_magnetic_permeability.txt &

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

#!/bin/sh

output_folder=research/output/derived_constants

# stefan_boltzmann_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?sigma|search_for=stefan
python ./main.py --target-value "5.670374419E-8" --target-unit "kg/(s^3 K^4)" > ./$output_folder/stefan_boltzmann_constant.txt &

# rydberg_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?ryd|search_for=rydberg+constant
python ./main.py --target-value "1.0973731568160(21)e+7" --target-unit "1/m" > ./$output_folder/rydberg_constant.txt &

# fine_structure_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?alph|search_for=fine+structure+constant
python ./main.py --target-value "7.2973525693(11)E-3" --target-unit "" > ./$output_folder/fine_structure_constant.txt &

# magnetic_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?mu0|search_for=vacuum+permeability
python ./main.py --target-value "1.25663706212(19)e-6" --target-unit "m kg/(A^2 s^2)" > ./$output_folder/magnetic_constant.txt &

# molar_gas_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?r|search_for=molar+gas+constant
python ./main.py --target-value "8.314462618E0" --target-unit "(kg m^2)/(K mol s^2)" > ./$output_folder/molar_gas_constant.txt &

# wien_frequency_displacement_law_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?bpwien|search_for=wien_frequency+displacement+law+constant
python ./main.py --target-value "5.878925757E+10" --target-unit "1/(K s)" > ./$output_folder/wien_frequency_displacement_law_constant.txt &

# impedance_of_free_space. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?z0|search_for=characteristic+impedance+of+vacuum
python ./main.py --target-value "3.76730313668(57)E+2" --target-unit "(kg m^2)/(s^3 A^2)" > ./$output_folder/impedance_of_free_space.txt &

# josephson_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?kjos|search_for=josephson
python ./main.py --target-value "4.835978484E+14" --target-unit "(A s^2)/(kg m^2)" > ./$output_folder/josephson_constant.txt &

# von_klitzing_constant. Ref: https://physics.nist.gov/cgi-bin/cuu/Value?rk|search_for=von+Klitzing+constant
python ./main.py --target-value "2.581280745E+4" --target-unit "(kg m^2)/(A^2 s^3)" > ./$output_folder/von_klitzing_constant.txt &

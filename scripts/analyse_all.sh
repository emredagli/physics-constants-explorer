#!/bin/sh

# stefan_boltzmann_constant
python ./main.py --target-value "5.670374E-8" --target-unit "kg/(s^3 K^4)" > ./scripts/outputs/analyse_all/stefan_boltzmann_constant.txt &
# rydberg_constant
python ./main.py --target-value "1.09737315e+7" --target-unit "1/m" > ./scripts/outputs/analyse_all/rydberg_constant.txt &
# fine_structure_constant
python ./main.py --target-value "7.29735256E-3" --target-unit "" > ./scripts/outputs/analyse_all/fine_structure_constant.txt &
# newtonian_constant_of_gravitation
python ./main.py --target-value "6.6743e-11" --target-unit "m^3/(kg s^2)" > ./scripts/outputs/analyse_all/newtonian_constant_of_gravitation.txt &
# vacuum_permeability
python ./main.py --target-value "1.256637062e-6" --target-unit "m kg/(A^2 s^2)" > ./scripts/outputs/analyse_all/vacuum_permeability.txt &
# molar_gas_constant
python ./main.py --target-value "8.3144626E0" --target-unit "(kg m^2)/(K mol s^2)" > ./scripts/outputs/analyse_all/molar_gas_constant.txt &
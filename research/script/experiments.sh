#!/bin/sh

output_folder=research/output/experiments
config_folder=research/config/experiments

# Magnetic Constant to Electric Constant Ratio,
python ./main.py --target-value "1.4192572923(42)E+5" \
                 --target-unit "(kg^2 m^4)/(A^4 s^6)" \
                 --config-file "$config_folder/magnetic_constant_to_electric_constant_ratio.json" \
                 > $output_folder/magnetic_constant_to_electric_constant_ratio.txt &

# Newtonian Constant of Gravitation - Attempt 01
python ./main.py --target-value "6.67430(15)e-11" \
                 --target-unit "m^3/(kg s^2)" \
                 --config-file "$config_folder/newtonian_constant_of_gravitation_attempt_01.json" \
                 > $output_folder/newtonian_constant_of_gravitation_attempt_01.txt &

# Newtonian Constant of Gravitation - Attempt 02
python ./main.py --target-value "6.67430(15)e-11" \
                 --target-unit "m^3/(kg s^2)" \
                 --config-file "$config_folder/newtonian_constant_of_gravitation_attempt_02.json" \
                 > $output_folder/newtonian_constant_of_gravitation_attempt_02.txt &

# Newtonian Constant of Gravitation - Attempt 02 with Brute Force
#python ./main.py --target-value "6.67430(15)e-11" \
#                 --target-unit "m^3/(kg s^2)" \
#                 --config-file "$config_folder/newtonian_constant_of_gravitation_attempt_02_brute.json" \
#                 > $output_folder/newtonian_constant_of_gravitation_attempt_02_brute.txt &

# Neutron mean life Article - http://aesop.phys.utk.edu/ph611/2012/projects/Hayes.pdf
python ./main.py --target-value "8.796(8)e2" \
                 --target-unit "s" \
                 --config-file "$config_folder/neutron_mean_life.json" \
                 > $output_folder/neutron_mean_life.txt &
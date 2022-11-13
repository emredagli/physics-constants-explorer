#!/bin/sh

output_folder=research/output/experiments
config_folder=research/config/experiments
definition_file=research/definition/default_en.txt

# Magnetic Constant to Electric Constant Ratio,
python ./main.py --target-value "1.4192572923(42)E+5" \
                 --target-unit "(kg^2 m^4)/(A^4 s^6)" \
                 --config-file "$config_folder/magnetic_constant_to_electric_constant_ratio.json" \
                 --definition-file $definition_file \
                 > $output_folder/magnetic_constant_to_electric_constant_ratio.txt &

# Newtonian Constant of Gravitation - Attempt 01
python ./main.py --target-value "6.67430(15)e-11" \
                 --target-unit "m^3/(kg s^2)" \
                 > $output_folder/newtonian_constant_of_gravitation_attempt_01.txt &

# Newtonian Constant of Gravitation - Attempt 02
python ./main.py --target-value "6.67430(15)e-11" \
                 --target-unit "m^3/(kg s^2)" \
                 --config-file "$config_folder/newtonian_constant_of_gravitation_attempt_02.json" \
                 --definition-file $definition_file \
                 > $output_folder/newtonian_constant_of_gravitation_attempt_02.txt &

# Newtonian Constant of Gravitation - Attempt 03
python ./main.py --target-value "6.67430(15)e-11" \
                 --target-unit "m^3/(kg s^2)" \
                 --config-file "$config_folder/newtonian_constant_of_gravitation_attempt_03.json" \
                 --definition-file $definition_file \
                 > $output_folder/newtonian_constant_of_gravitation_attempt_03.txt &

# Newtonian Constant of Gravitation - Attempt 04
python ./main.py --target-value "6.67430(15)e-11" \
                 --target-unit "m^3/(kg s^2)" \
                 --config-file "$config_folder/newtonian_constant_of_gravitation_attempt_04_plank_units.json" \
                 --definition-file $definition_file \
                 > $output_folder/newtonian_constant_of_gravitation_attempt_04.txt &

# config_black_hole_density
#python ./main.py --target-value "2.0826698222E+56" \
#                 --target-unit "(kg m^3)/s^4" \
#                 --config-file "$config_folder/black_hole_density.json" \
#                 --definition-file $definition_file \
#                 > $output_folder/black_hole_density.txt &


#python ./main.py --target-value "2.0828258556E+45" --target-unit "(kg m^3)/s^4"
#python ./main.py --target-value "2.0826698222E+56" --target-unit "(kg m^3)/s^4"

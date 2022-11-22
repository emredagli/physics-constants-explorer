#!/bin/sh

output_folder=research/output/physics_problems
config_folder=research/config/physics_problems

# Black Hole Density
python ./main.py --target-value "2.0826698222E+56" \
                 --target-unit "(kg m^3)/s^4" \
                 --config-file "$config_folder/black_hole_density.json" \
                 > $output_folder/black_hole_density.txt &

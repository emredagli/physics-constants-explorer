#!/bin/sh

output_folder=research/output/constant_tests
config_folder=research/config/constant_tests

## Proton to Electron Mass Ratio (in terms of pi :)
#python ./main.py --target-value "1.83612(5)E3" --target-unit "" > ./$output_folder/proton_to_electron_mass_ratio.txt &

# The Height of a Giraffe / D.N. Page
python ./main.py --target-value "2.44" \
                 --target-unit "m" \
                 --config-file "$config_folder/the_height_of_a_giraffe.json" \
                 > $output_folder/the_height_of_a_giraffe.txt &

## Chirpy mass - Ref: Observation of Gravitational Waves from a Binary Black Hole Merger / B. P. Abbott et al
#python ./main.py --target-value "1.098084728279E+34" \
#                 --target-unit "kg/s" \
#                 --config-file "$config_folder/chirp_mass.json" \
#                 > $output_folder/chirp_mass.txt &
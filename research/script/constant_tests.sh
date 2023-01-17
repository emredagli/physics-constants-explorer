#!/bin/sh

output_folder=research/output/constant_tests
config_folder=research/config/constant_tests

# Proton to Electron Mass Ratio (in terms of pi :)
python ./main.py --target-value "1.83612(5)E3" --target-unit "" > ./$output_folder/proton_to_electron_mass_ratio.txt &

# The Height of a Giraffe / D.N. Page
python ./main.py --target-value "2.44" \
                 --target-unit "m" \
                 --config-file "$config_folder/the_height_of_a_giraffe.json" \
                 > $output_folder/the_height_of_a_giraffe.txt &

# Chirp mass - Ref: Observation of Gravitational Waves from a Binary Black Hole Merger / B. P. Abbott et al
python ./main.py --target-value "1.098084728279E+34" \
                 --target-unit "kg/s" \
                 --config-file "$config_folder/chirp_mass.json" \
                 > $output_folder/chirp_mass.txt &

# Black hole density in terms of T (orbital period) and r (radius of black hole)
# Ref: https://github.com/emredagli/physics-constants-explorer/blob/main/research/img.png
# numeric_calculator.py result of black_hole_density.json is 2.082669822279E+56 kg·m³/s⁴
python ./main.py --target-value "2.082669822279E+56" \
                 --target-unit "kg m^3 / s^4" \
                 --config-file "$config_folder/black_hole_density.json" \
                 > $output_folder/black_hole_density.txt &
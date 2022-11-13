#!/bin/sh

output_folder=research/output/physics_problems
config_folder=research/config/physics_problems
definition_file=research/definition/default_en.txt

# Black Hole Density
python ./main.py --target-value "2.0826698222E+56" \
                 --target-unit "(kg m^3)/s^4" \
                 --config-file "$config_folder/black_hole_density.json" \
                 --definition-file $definition_file \
                 > $output_folder/black_hole_density.txt &

# Mid-ocean Tide Range
# Used Constants:
# mass_of_earth: 5.9722(6)E+24 kg --- https://en.wikipedia.org/wiki/Earth_mass
# mass_of_moon: 7.342E+22 kg --- https://en.wikipedia.org/wiki/Moon
# radius_of_earth: 6.367(17)E+6 m, a = 6378137 m and b = 6356752.3142 m --- https://en.wikipedia.org/wiki/Earth_radius
# distance_earth_and_moon: 3.84(25)E+8 m --- https://en.wikipedia.org/wiki/Lunar_distance_(astronomy)

python ./main.py --target-value "5.4(1)E-1" \
                 --target-unit "m" \
                 --config-file "$config_folder/mid_ocean_tide_range.json" \
                 --definition-file $definition_file \
                 > $output_folder/mid_ocean_tide_range.txt &
#python ./main.py --target-value "2.0828258556E+45" --target-unit "(kg m^3)/s^4"
#python ./main.py --target-value "2.0826698222E+56" --target-unit "(kg m^3)/s^4"

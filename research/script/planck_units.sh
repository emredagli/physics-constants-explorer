#!/bin/sh

output_folder=research/output/planck_units
config_folder=research/config/planck_units

# Planck length, Ref: https://physics.nist.gov/cgi-bin/cuu/Value?plkl
python ./main.py --target-value "1.616255(18)E-35" \
                 --target-unit "m" \
                 --config-file "$config_folder/plank_units.json" \
                 > $output_folder/planck_length.txt &

# Planck mass, Ref: https://physics.nist.gov/cgi-bin/cuu/Value?plkm
python ./main.py --target-value "2.176434(24)E-8" \
                 --target-unit "kg" \
                 --config-file "$config_folder/plank_units.json" \
                 > $output_folder/planck_mass.txt &

# Planck time, Ref: https://physics.nist.gov/cgi-bin/cuu/Value?plkt
python ./main.py --target-value "5.391247(60)E-44" \
                 --target-unit "s" \
                 --config-file "$config_folder/plank_units.json" \
                 > $output_folder/planck_time.txt &

# Planck temperature, Ref: https://physics.nist.gov/cgi-bin/cuu/Value?plktmp
python ./main.py --target-value "1.416784(16)E+32" \
                 --target-unit "K" \
                 --config-file "$config_folder/plank_units.json" \
                 > $output_folder/planck_temperature.txt &

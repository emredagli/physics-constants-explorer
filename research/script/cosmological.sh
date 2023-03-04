#!/bin/sh

output_folder=research/output/cosmological
config_folder=research/config/cosmological

# Cosmological constant, Λ, Ref: https://en.wikipedia.org/wiki/Cosmological_constant
python ./main.py --target-value "1.106(23)E-52" \
                 --target-unit "m^-2" \
                 --config-file "$config_folder/cosmological_constant.json" \
                 > "$output_folder/cosmological_constant.txt"
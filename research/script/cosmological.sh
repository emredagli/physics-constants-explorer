#!/bin/sh

output_folder=research/output/cosmological
config_folder=research/config/cosmological

# Cosmological constant, Λ, Ref: https://en.wikipedia.org/wiki/Cosmological_constant
python ./main.py --target-value "1.106(23)E-52" \
                 --target-unit "m^-2" \
                 --config-file "$config_folder/cosmological_constant.json" \
                 > "$output_folder/cosmological_constant.txt"

# kappa - the Einstein gravitational constant (8 pi G / c^4): 2.07664744 × 10-43 m^-1 kg^-1 s^2
python ./main.py --target-value "2.07664744E-43" \
                 --target-unit "s^2 / (kg m)" \
                 --config-file "$config_folder/einstein_gravitational_constant.json" \
                 > "$output_folder/einstein_gravitational_constant.txt"
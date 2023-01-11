import json
import time

import requests

from src.codata_extractor import RESULT_FILE_PATH, ALL_CONSTANTS_DIRECTORY

with open(RESULT_FILE_PATH, 'r') as f:
    constants: dict = json.load(f)

for index, key in enumerate(constants.keys()):
    page = requests.get(constants[key].get("codata"))
    with open(f"{ALL_CONSTANTS_DIRECTORY}{key}.html", 'w') as f:
        f.write(page.text)
    print(f"{str(index+1)} - {key} downloaded, size {len(page.text)}.")
    time.sleep(0.05)

print(f"Total: {len(constants.keys())}")

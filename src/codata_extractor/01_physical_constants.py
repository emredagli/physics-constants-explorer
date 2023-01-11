import requests
from src.codata_extractor import ALL_CONSTANTS_LIST_FILE_PATH

URL = "https://physics.nist.gov/cgi-bin/cuu/Category?view=html&All+values.x=62&All+values.y=14"
page = requests.get(URL)

with open(ALL_CONSTANTS_LIST_FILE_PATH, 'w') as f:
    f.write(page.text)

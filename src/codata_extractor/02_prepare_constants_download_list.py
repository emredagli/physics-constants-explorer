import json

from bs4 import BeautifulSoup

from src.codata_extractor import ALL_CONSTANTS_LIST_FILE_PATH, RESULT_FILE_PATH

# Broken links
LINKS_IGNORE_LIST = ["/cgi-bin/cuu/Value?am"]

with open(ALL_CONSTANTS_LIST_FILE_PATH) as f:
    content = f.readlines()
    content = "\n".join(content)

soup = BeautifulSoup(content, "html.parser")

links = soup.find_all(name="a")

constants = dict()

for link in links:
    link_url: str = link["href"]
    link_text: str = link.text.strip().lower()

    if not link_url.startswith("/cgi-bin/cuu/Value?"):
        continue

    link_url = link_url.split("|", 1)[0]
    if link_url in LINKS_IGNORE_LIST:
        continue

    key_val = link_text.replace(" ", "_").replace("-", "_").replace("/", "_")

    constants[key_val] = {
        "name": link_text.capitalize(),
        "codata": f"https://physics.nist.gov{link_url}"
    }

print(len(constants.keys()))
with open(RESULT_FILE_PATH, 'w') as f:
    f.write(json.dumps(constants, indent=2))

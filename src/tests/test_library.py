import pathlib
import json


def get_test_resources(method="brute_force"):
    test_resources_path = str(pathlib.Path(__file__).parent.resolve()) + '/test_resources'

    # Reading config
    with open(f"{test_resources_path}/config.json") as f:
        config = json.load(f)
    config["method"] = method

    # Reading definition
    with open(f"{test_resources_path}/definition.json") as f:
        definition = json.load(f)

    return config, definition

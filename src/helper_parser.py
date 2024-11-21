"""
=======================================================================

 File: helper_parser.py


 Description: Parses the API json files and creates a new API folder
 -             with only the necessary files.

=======================================================================
"""

# System includes
import json

# Project includes
import loader
from handler import Handler


def build_pkmn_types():
    handler = Handler()

    result = {}
    for pkmn in handler.data.lists["pokemon"]:
        pkmn_name = pkmn.get("name")
        type1, type2 = handler.get_type(pkmn_name)
        result[pkmn_name] = (type1, type2)

    write_file("pokemon_types", result)


def build_type_interactions():
    handler = Handler()

    result = {}
    for pkmn_type in handler.data.lists["type"]:
        type_name = pkmn_type.get("name")
        result[type_name] = handler.get_type_interactions(type_name, None)

    write_file("type_interactions", result)


def write_file(name: str, result: dict[str, tuple[str, str] | list[float, float]]):
    with open(f"{name}.json", "w") as f:
        json.dump(result, f)
    print(f"created file {name}json.")


if __name__ == "__main__":
    build_pkmn_types()
    build_type_interactions()

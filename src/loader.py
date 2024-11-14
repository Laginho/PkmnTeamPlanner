"""
=========================================================================

 File: loader.py


 Description: Handles loading of the API json files.

========================================================================
"""

# System includes
import json


PATH = "../api/v2"


TYPES = [
    "normal",
    "fighting",
    "flying",
    "poison",
    "ground",
    "rock",
    "bug",
    "ghost",
    "steel",
    "fire",
    "water",
    "grass",
    "electric",
    "psychic",
    "ice",
    "dragon",
    "dark",
    "fairy",
]


def load_folder(folder_name: str) -> dict:
    with open(f"{PATH}/{folder_name}/index.json") as f:
        return json.load(f)


def load_dict_from_num(folder_name: str, num: str) -> dict:
    """Looks up a pokemon or type dict by its number

    Args:
        folder_name (str): "pokemon" or "type"
        num (str): the entry's number

    Returns:
        dict: the entry from the json file
    """
    with open(f"{PATH}/{folder_name}/{num}/index.json") as f:
        return json.load(f)

"""
=========================================================================

 File: loader.py


 Description: Handles loading of the API json files.

========================================================================
"""

# System includes
import json
import os

os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}/../")
PATH = "api"


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


def load_dict(folder_name: str) -> dict:
    """Get the corresponding dict from the json file."""

    with open(f"{PATH}/{folder_name}.json") as f:
        return json.load(f)

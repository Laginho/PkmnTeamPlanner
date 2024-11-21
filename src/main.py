"""
=======================================================================

 File: main.py

 Description: Main project file, which puts the project together.

 TODO: ver 2.0
       [ ] Fix: Refactor to use new json files.
       [ ] Add: Error handling.
       [ ] Add: File documentation and docstrings.

=======================================================================
"""

# system includes
from handler import Handler

# project includes
from interface import Interface

MODE = "proper"


def raw_run():
    handler = Handler()

    pkmn_list = [
        "arcanine",
        "stoutland",
        "scrafty",
        "excadrill",
        "leavanny",
        "cofagrigus",
    ]

    ints = {}

    for pkmn in pkmn_list:
        ints = handler.get_pkmn_interactions(pkmn)
        print(f"\n\n{pkmn}: {ints}")


def proper_run(debug=False):
    interface = Interface(debug)


if __name__ == "__main__":
    if MODE == "raw":
        raw_run()
    if MODE == "proper":
        proper_run()
    if MODE == "debug":
        proper_run(debug=True)
    else:
        print("Invalid MODE.")

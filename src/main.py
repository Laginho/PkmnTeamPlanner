from handler import Handler

if __name__ == "2":
    handler = Handler()

    pkmn = "arcanine"
    print(f"pkmn: {pkmn}. type: {handler.get_type(pkmn)}")
    t1, t2 = handler.get_type(pkmn)

    a = handler.get_type_interactions(t1, t2)
    print(a)

if __name__ == "__main__":
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
        t1, t2 = handler.get_type(pkmn)
        ints = handler.get_type_interactions(t1, t2)
        print(f"\n\n{pkmn}: {ints}")

    print(ints)

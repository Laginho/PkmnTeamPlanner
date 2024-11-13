import pokebase as pb


def get_type(pkmn):
    try:
        a = pb.pokemon(pkmn)
        return a.types[0].type
    except AttributeError:
        return None


print(get_type("pikachu"))

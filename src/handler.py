# system includes
import numpy

# project includes
import loader


class Handler:
    def __init__(self):
        self.pkmn_dict = loader.load_dict("pokemon")
        self.types_dict = loader.load_dict("type")

    def pkmn_is_valid(self, pkmn: str) -> bool:
        for pkmn_name in self.pkmn_dict.keys():
            if pkmn_name == pkmn.lower():
                return True

        return False

    def get_type(self, pkmn: str) -> tuple[str, str]:
        return self.pkmn_dict.get(pkmn)

    def get_type_interactions(
        self, type1: str, type2: str
    ) -> dict[str, list[float, float]]:

        ints_type1 = self.types_dict.get(type1)
        ints_type2 = self.types_dict.get(type2)

        interactions = {}  # (fire) {"bug": [2, 0.5]}

        for int_dict in [ints_type1, ints_type2]:
            if not int_dict:
                break

            for int_type in int_dict:
                if not interactions.get(int_type):
                    interactions[int_type] = [1.0, 1.0]

                int_values = int_dict.get(int_type)
                interactions[int_type] = schur(interactions[int_type], int_values)

                if interactions.get(int_type)[0] == 4.0:
                    interactions[int_type][0] = 2.0
                if interactions.get(int_type)[0] < 1.0:
                    interactions[int_type][0] = 1.0
                if interactions.get(int_type)[0] == 0.25:
                    interactions[int_type][0] = 0.5

        return interactions

    def get_pkmn_interactions(self, pkmn) -> dict[str, list[float, float]]:
        types = self.get_type(pkmn)
        return self.get_type_interactions(*types)

    def get_team_interactions(self, team: list[str]) -> dict[str, list[float, float]]:
        interactions = {}

        for pkmn in team:
            inters = self.get_pkmn_interactions(pkmn)

            for inter_key, inter_values in inters.items():
                if not interactions.get(inter_key):
                    interactions[inter_key] = inter_values

                else:
                    interactions[inter_key][0] = max(
                        interactions[inter_key][0], inter_values[0]
                    )

                    interactions[inter_key][1] = min(
                        interactions[inter_key][1], inter_values[1]
                    )

        return interactions

    def is_complete(self, interactions: dict[str, list[float, float]]) -> str:
        missing_hard = []
        missing_soft = []
        for type_ in loader.TYPES:
            if not interactions.get(type_):
                missing_hard.append([type_, [1.0, 1.0]])
                missing_soft.append([type_, [1.0, 1.0]])
            else:
                attack = interactions[type_][0]
                defense = interactions[type_][1]
                if attack < 1.0 or defense > 1.0:
                    missing_hard.append([type_, [attack, defense]])
                elif attack < 2.0 or defense > 0.5:
                    missing_soft.append([type_, [attack, defense]])

        if missing_hard or missing_soft:
            str1 = "Not complete." if missing_hard else "Almost complete."
            str2 = "\n\nHard problems:\n"
            str3 = "\n\nSoft problems:\n"

            if missing_hard:
                for missing_item in missing_hard:
                    str2 += f"{missing_item[0]}: {missing_item[1]}\n"
            if missing_soft:
                for missing_item in missing_soft:
                    str3 += f"{missing_item[0]}: {missing_item[1]}\n"

            return str1 + str2 + str3

        return "Complete!"


def schur(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return a if len(a) > len(b) else b

    a, b = numpy.array(a), numpy.array(b)

    return list(a * b)

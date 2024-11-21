from data import Data
from loader import TYPES


class Handler:
    def __init__(self):
        self.data = Data("pokemon", "type")

    def pkmn_is_valid(self, pkmn: str) -> bool:
        pkmn_list = self.data.lists["pokemon"]
        is_valid = pkmn in (pkmn_info.get("name") for pkmn_info in pkmn_list)

        return is_valid

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

    def get_type(self, pkmn: str) -> tuple[str, str]:
        num = self.data.get_num_from_name("pokemon", pkmn)
        pkmn = self.data.get_dict_from_num("pokemon", num)

        if not pkmn:
            print(f"Pokemon {pkmn} not found")
            return
        else:
            type_list = pkmn.get("types")
            types = []
            for slot in type_list:
                types.append(slot.get("type").get("name"))

            if len(types) == 1:
                types.append(None)

            return tuple(types)

    def get_type_interactions(self, type1, type2) -> dict[str, list[float, float]]:
        num1 = self.data.get_num_from_name("type", type1)
        num2 = self.data.get_num_from_name("type", type2)
        type1 = self.data.get_dict_from_num("type", num1)
        type2 = self.data.get_dict_from_num("type", num2)

        if not type2:
            type2 = {"damage_relations": {}}

        interactions = {}  # (fire) {"bug": [2, 0.5]}

        relation_sets = [
            type1.get("damage_relations").items(),
            type2.get("damage_relations").items(),
        ]

        for relation_set in relation_sets:
            for relation_type, relation_list in relation_set:
                for relation in relation_list:
                    relation = relation.get("name")

                    if not interactions.get(relation):
                        interactions[relation] = [1.0, 1.0]

                    if relation_type == "double_damage_from":
                        interactions[relation][1] *= 2.0
                    if relation_type == "half_damage_from":
                        interactions[relation][1] *= 0.5
                    if relation_type == "no_damage_from":
                        interactions[relation][1] *= 0.0
                    if relation_type == "double_damage_to":
                        interactions[relation][0] = max(2.0, interactions[relation][0])
                    if relation_type == "half_damage_to":
                        interactions[relation][0] = max(0.5, interactions[relation][0])
                    if relation_type == "no_damage_to":
                        interactions[relation][0] = max(0.0, interactions[relation][0])

                    # Can't deal 4x nor 0.25x on one type
                    if interactions[relation][0] == 4.0:
                        interactions[relation][0] = 2.0
                    if interactions[relation][0] == 0.25:
                        interactions[relation][0] = 0.5

        return interactions

    def is_complete(self, interactions: dict[str, list[float, float]]) -> str:
        missing_hard = []
        missing_soft = []
        for type_ in TYPES:
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
            str1 = "Not complete." if missing_soft else "Almost complete."
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

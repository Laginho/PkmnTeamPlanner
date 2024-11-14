from data import Data
from loader import TYPES


class Handler:
    def __init__(self):
        self.data = Data("pokemon", "type")

    def get_type(self, pkmn: str) -> tuple[str, str]:
        num = self.get_num_from_name("pokemon", pkmn)
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

    def get_type_interactions(self, type1, type2) -> list:
        num1 = self.get_num_from_name("type", type1)
        num2 = self.get_num_from_name("type", type2)
        type1 = self.data.get_dict_from_num("type", num1)
        type2 = self.data.get_dict_from_num("type", num2)

        interactions = {}
        for relation_type, relation_list in type1.get("damage_relations").items():
            interactions[relation_type] = []
            for relation in relation_list:
                interactions[relation_type].append(relation.get("name"))

        return interactions

    def get_num_from_name(self, folder_name: str, name: str) -> str:
        results = self.data.lists[folder_name]

        for item in results:
            if item.get("name") == name:
                url = item.get("url")  # "/api/v2/pokemon/587/"
                return url.split("/")[-2]  # 587

        return None

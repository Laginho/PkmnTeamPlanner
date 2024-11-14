import loader


class Data:
    def __init__(self, *args):
        self._data: dict[str, dict] = {}
        self.folders = args
        for arg in args:
            self._load_data(arg)

    def _load_data(self, folder: str) -> None:
        assert isinstance(folder, str), f"Expected str, got {type(folder)}"

        try:
            self._data[folder] = loader.load_folder(folder)

        except KeyError:
            print(f"Folder {folder} not found")

    def get_dict_from_num(self, folder_name: str, num: str) -> dict:
        if not num:
            return

        name = self._data[folder_name]

        if name.get(num):
            return name[num]

        else:
            name[num] = loader.load_dict_from_num(folder_name, num)
            return name[num]

    @property
    def lists(self) -> list[dict]:
        return {
            "pokemon": self._data.get("pokemon").get("results"),
            "type": self._data.get("type").get("results"),
        }

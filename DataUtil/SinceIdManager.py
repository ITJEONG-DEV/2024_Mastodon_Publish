import os

current_path = os.path.dirname(os.path.abspath(__file__))


class SinceIdManager:
    def __init__(self):
        self.__since_id = -1
        self.__load()

    @property
    def since_id(self):
        return self.__since_id

    @since_id.setter
    def since_id(self, since_id):
        self.__since_id = since_id
        self.__save()

    def __load(self):
        with open(f"{current_path}/Data/since_id.txt", "r") as txt:
            self.__since_id = txt.read().strip()

    def __save(self):
        with open(f"{current_path}/Data/since_id.txt", "w") as txt:
            txt.write(str(self.__since_id))

import os
import json

current_path = os.path.dirname(os.path.abspath(__file__))


class IdMatcher:
    def __init__(self):
        self.__load()

    def __save(self):
        with open(f"{current_path}/Data/bridge_to_bot.json", "w") as json_file:
            json.dump(self.bridge_to_bot, json_file)

        with open(f"{current_path}/Data/bot_to_bridge.json", "w") as json_file:
            json.dump(self.bot_to_bridge, json_file)

        with open(f"{current_path}/Data/bot_mention_info.json", "w") as json_file:
            json.dump(self.bot_mention_info, json_file)

    def __load(self):
        with open(f"{current_path}/Data/bridge_to_bot.json", "r") as json_file:
            self.bridge_to_bot = json.load(json_file)

        with open(f"{current_path}/Data/bot_to_bridge.json", "r") as json_file:
            self.bot_to_bridge = json.load(json_file)

        with open(f"{current_path}/Data/bot_mention_info.json", "r") as json_file:
            self.bot_mention_info = json.load(json_file)

    def add(self, bridge_id, bot_id):
        self.bridge_to_bot[bridge_id] = bot_id
        self.bot_to_bridge[bot_id] = bridge_id

        self.__save()

    def add_user_id_for_mention(self, bot_id, user_id):
        self.bot_mention_info[bot_id] = user_id

    def get_user_id_for_mention(self, bot_id):
        if bot_id not in self.bot_mention_info:
            return None

        return self.bot_mention_info[bot_id]

    def get_bridge_id(self, bot_id):
        if bot_id not in self.bot_to_bridge.keys():
            return None

        return self.bot_to_bridge[bot_id]

    def get_bot_id(self, bridge_id):
        if bridge_id not in self.bridge_to_bot.keys():
            return None

        return self.bridge_to_bot[bridge_id]

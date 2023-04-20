from typing import List

from GoldyBot import Goldy
from GoldyBot.config import Config

class DemolitionConfig(Config):
    def __init__(self, goldy: Goldy):
        # I'm using the goldy.json file as the configuration file for this extension.
        super().__init__(goldy.config.json_path)

    @property
    def guild_to_nuke(self) -> str:
        """Returns the code_name of the guild that should be nuked."""
        return self.get("demolition_bot", "guild_to_nuke", default_value = None)
    
    @property
    def channels_to_ignore(self) -> List[str]:
        """Returns a list of ids of channels that the bot should exclude from nuking."""
        return self.get("demolition_bot", "channels_to_ignore", default_value = [])
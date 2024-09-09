import datetime
from typing import Literal, Dict

class CooldownService:
    def __init__(self):
        # Dictionary to hold cooldowns for each player and action
        self.cooldowns: Dict[str, Dict[int, datetime.datetime]] = {
            "attack": {},
            "cast_spell": {}
        }

    def set_cooldown(self, discord_id: int, action: Literal["attack", "cast_spell"], duration: int):
        """
        Sets a cooldown for a player for the specified action.

        :param discord_id: The player's Discord ID.
        :param action: The action for which to set the cooldown (e.g., 'attack' or 'cast_spell').
        :param duration: The cooldown duration in seconds.
        """
        current_time = datetime.datetime.now(datetime.timezone.utc)
        expiration_time = current_time + datetime.timedelta(seconds=duration)
        self.cooldowns[action][discord_id] = expiration_time

    def is_on_cooldown(self, discord_id: int, action: Literal["attack", "cast_spell"]) -> bool:
        """
        Checks if a player is currently on cooldown for the specified action.

        :param discord_id: The player's Discord ID.
        :param action: The action to check cooldown for (e.g., 'attack' or 'cast_spell').
        :return: True if the player is on cooldown, False otherwise.
        """
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if discord_id in self.cooldowns[action]:
            cooldown_end = self.cooldowns[action][discord_id]
            if current_time < cooldown_end:
                return True
        return False

    def get_cooldown_expiration(self, discord_id: int, action: Literal["attack", "cast_spell"]) -> datetime.datetime | None:
        """
        Retrieves the expiration time of the cooldown for a player and action.

        :param discord_id: The player's Discord ID.
        :param action: The action for which to retrieve the cooldown expiration.
        :return: The expiration datetime if on cooldown, or None if not on cooldown.
        """
        if discord_id in self.cooldowns[action]:
            return self.cooldowns[action][discord_id]
        return None

    def clear_cooldown(self, discord_id: int, action: Literal["attack", "cast_spell"]):
        """
        Clears the cooldown for a player and action.

        :param discord_id: The player's Discord ID.
        :param action: The action for which to clear the cooldown.
        """
        if discord_id in self.cooldowns[action]:
            del self.cooldowns[action][discord_id]

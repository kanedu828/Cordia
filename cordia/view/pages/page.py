from abc import ABC, abstractmethod
import discord

from cordia.service.cordia_service import CordiaService


class Page(ABC):
    def __init__(self, cordia_service: CordiaService, discord_id: int):
        self.cordia_service = cordia_service
        self.discord_id = discord_id

    @abstractmethod
    async def render(self, interaction: discord.Interaction):
        """Render the page, must be implemented by subclasses."""
        pass

    @abstractmethod
    async def _create_view(self):
        pass

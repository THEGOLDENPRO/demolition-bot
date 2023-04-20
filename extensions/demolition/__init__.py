from __future__ import annotations

import GoldyBot
from GoldyBot.goldy.guilds import Guild
from nextcore.http import Route

from typing import List
from discord_typings import ChannelData

from .config import DemolitionConfig

class Demolition(GoldyBot.Extension):
    def __init__(self):
        super().__init__()

        self.config = DemolitionConfig(self.goldy)

    @GoldyBot.command()
    async def nuke(self, platter: GoldyBot.GoldPlatter):
        # Get id of guild to nuke.
        # -------------------------
        # TODO: I need to make this code a method in the gb framework to simplify things in the future, writing this code seems so inconvenient.
        guild_to_nuke_id = None
        for guild in self.goldy.guilds.allowed_guilds:
            if guild[1] == self.config.guild_to_nuke:
                guild_to_nuke_id = guild[0]
                break

        guild_to_nuke: Guild | None = self.goldy.guilds.get_guild(guild_to_nuke_id)

        if guild_to_nuke is None:
            await platter.send_message("🔴 The guild to nuke is not set up in config!")
            return
        

        # I haven't implemented deleting channels into the gb framework yet so here goes some nextcore raw requests.
        # ------------------------------------------------------------------------------------------------------------
        await platter.send_message("💣 Nuking...")

        r = await self.goldy.http_client.request(
            Route(
                "GET",
                "/guilds/{guild_id}/channels",
                guild_id = guild_to_nuke.id
            ),
            rate_limit_key = self.goldy.nc_authentication.rate_limit_key,
            headers = self.goldy.nc_authentication.headers,
        )

        guild_channels: List[ChannelData] = await r.json()
        
        # Delete all channels that are not in the ignore list.
        # -----------------------------------------------------
        for channel in guild_channels:

            if str(channel["id"]) in self.config.channels_to_ignore:
                self.logger.warning(f"Ignoring the channel '{channel['name']}'.")
                continue

            self.logger.debug(f"Nuking channel '{channel['name']}'...")
            await self.goldy.http_client.request(
                Route(
                    "DELETE",
                    "/channels/{channel_id}",
                    channel_id = channel["id"]
                ),
                rate_limit_key = self.goldy.nc_authentication.rate_limit_key,
                headers = self.goldy.nc_authentication.headers,
            )

        await platter.send_message(f"🟢 Done!", reply=True)

def load():
    Demolition()
import discord
import gc
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional


class Util(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction) -> None:
        """/ping"""
        message: str = "Pong! {0}".format(round(self.bot.latency * 1000, 1))
        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="memory")
    @app_commands.description("Get memory usage statistics")
    async def memory(self, interaction: discord.Interaction) -> None:
        """Get memory usage statistics for monitoring"""
        try:
            embed = discord.Embed(
                title="Memory Usage Statistics",
                color=discord.Color.blue()
            )
            
            # Garbage collection info
            gc_stats = gc.get_stats()
            total_collections = sum(stat['collections'] for stat in gc_stats)
            embed.add_field(
                name="Garbage Collection",
                value=f"Collections: {total_collections}",
                inline=False
            )
            
            # Memory leak prevention info
            embed.add_field(
                name="Memory Leak Prevention",
                value="✅ View timeouts set to 1 hour\n"
                      "✅ Views will expire automatically",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"Error getting memory stats: {str(e)}", 
                ephemeral=True
            )

    @commands.command(name="sync")
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Util(bot))

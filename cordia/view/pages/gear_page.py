from typing import List
from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance
from cordia.service.cordia_service import CordiaService
from cordia.util.decorators import only_command_invoker
from cordia.util.gear_util import display_gear_set_stats_for_set, get_gear_set_count
from cordia.util.text_format_util import snake_case_to_capital
from cordia.view.pages.page import Page
import discord
from discord.ui import Button, View, Select


class GearPage(Page):

    def __init__(self, cordia_service: CordiaService, discord_id: int):
        super().__init__(cordia_service, discord_id)
        self.armory_pages: List[discord.Embed] = []
        self.armory_page: int = -1  # -1 means we are on equipped gear page
        self.gear_type = "all"

    @classmethod
    async def create(
        cls,
        cordia_service: CordiaService,
        discord_id: int,
        type: GearType = None,
    ):
        """
        So we can initialize the armory_pages on page creation instead of
        having to constantly requery
        """
        gear_page = GearPage(cordia_service, discord_id)
        gear_page.armory_pages = await gear_page.paginate_gear(type)
        return gear_page

    async def render(self, interaction: discord.Interaction):
        view = self._create_view()
        embed = discord.Embed(title=f"Equipped Gear", color=discord.Color.blue())

        # Fetch the player's gear
        player_gear: List[GearInstance] = await self.cordia_service.get_player_gear(
            self.discord_id
        )

        # Create a dictionary to quickly look up gear by slot
        gear_dict = {gear.slot: gear for gear in player_gear}

        select_options = []
        # Add fields to the embed in the specified order
        for gear_type in GearType:
            gi = gear_dict.get(gear_type.value, None)
            if gi:
                gd = gi.get_gear_data()
                field_text = f"lv. {gd.level} {gd.name}"
                select_options.append(
                    discord.SelectOption(
                        label=snake_case_to_capital(gd.name), value=gi.id
                    )
                )
            else:
                field_text = "None"
            embed.add_field(
                name=gear_type.name.capitalize(), value=field_text, inline=False
            )

        gear_select = Select(
            placeholder="Select a gear to view",
            min_values=1,
            max_values=1,
            options=select_options,
            row=1,
        )
        gear_select.callback = self.gear_select_callback
        view.add_item(gear_select)
        # Send the response
        await interaction.response.edit_message(embed=embed, view=view)

    async def paginate_gear(self, type: GearType | None) -> List[List[GearInstance]]:
        gear: List[GearInstance] = await self.cordia_service.get_armory(self.discord_id)
        filtered_gear = [g for g in gear if not type or g.get_gear_data().type == type]
        filtered_gear.sort(key=lambda g: g.get_gear_data().level, reverse=True)
        page_size = 10
        return [
            filtered_gear[i : i + page_size]
            for i in range(0, len(filtered_gear), page_size)
        ]

    async def render_armory(self, interaction: discord.Interaction):
        view = self._create_armory_view()

        embed = discord.Embed(
            title=f"{self.gear_type.title()} Armory", color=discord.Color.blue()
        )

        if len(self.armory_pages) == 0:
            embed.add_field(name="", value=f"You dont have anything here", inline=False)
            await interaction.response.edit_message(embed=embed, view=view)
            return

        gear_list: List[GearInstance] = self.armory_pages[self.armory_page]

        embed.set_footer(text=f"Page {self.armory_page + 1}/{len(self.armory_pages)}")

        select_options = []
        for gear_item in gear_list:
            gd = gear_item.get_gear_data()
            # Format each gear item
            embed.add_field(
                name="", value=(f"**lv. {gd.level} {gd.name}**"), inline=False
            )
            select_options.append(
                discord.SelectOption(
                    label=snake_case_to_capital(gd.name), value=gear_item.id
                )
            )

        if len(gear_list) == 0:
            embed.add_field(
                name="",
                value=f"You have no {'armor' if self.gear_type == 'all' else self.gear_type}s",
                inline=False,
            )
        else:
            gear_select = Select(
                placeholder="Select a gear to view",
                min_values=1,
                max_values=1,
                options=select_options,
                row=1,
            )
            gear_select.callback = self.gear_select_callback
            view.add_item(gear_select)
        await interaction.response.edit_message(embed=embed, view=view)

    async def render_gear_sets_view(self, interaction: discord.Interaction):
        view = self._create_gear_sets_view()
        embed = discord.Embed(title=f"Gear Set Bonuses", color=discord.Color.blue())

        # Fetch the player's gear
        player_gear: List[GearInstance] = await self.cordia_service.get_player_gear(
            self.discord_id
        )

        gear_set_count = get_gear_set_count(player_gear)

        for gs in gear_set_count.keys():
            gear_stats_str = display_gear_set_stats_for_set(gs, gear_set_count[gs])

            embed.add_field(name=gs.replace("_", " ").title(), value=gear_stats_str)

        # Send the response
        await interaction.response.edit_message(embed=embed, view=view)

    def _create_view(self):
        view = View(timeout=None)

        equipped_gear_button = Button(
            label="Equipped Gear", style=discord.ButtonStyle.blurple, row=2
        )
        equipped_gear_button.disabled = True

        armory_button = Button(label="Armory", style=discord.ButtonStyle.blurple, row=2)
        armory_button.callback = self.armory_button_callback

        gear_sets_button = Button(
            label="Gear Sets", style=discord.ButtonStyle.blurple, row=2
        )
        gear_sets_button.callback = self.gear_sets_button_callback

        equip_highest_level_gear_button = Button(
            label="Equip Highest Level Gear", style=discord.ButtonStyle.green, row=2
        )
        equip_highest_level_gear_button.callback = (
            self.equip_highest_level_gear_button_callback
        )

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=3)
        back_button.callback = self.back_button_callback

        view.add_item(equipped_gear_button)
        view.add_item(armory_button)
        view.add_item(gear_sets_button)
        view.add_item(equip_highest_level_gear_button)
        view.add_item(back_button)

        return view

    def _create_gear_sets_view(self):
        view = View(timeout=None)

        equipped_gear_button = Button(
            label="Equipped Gear", style=discord.ButtonStyle.blurple, row=2
        )
        equipped_gear_button.callback = self.equipped_gear_button_callback

        armory_button = Button(label="Armory", style=discord.ButtonStyle.blurple, row=2)
        armory_button.callback = self.armory_button_callback

        gear_sets_button = Button(
            label="Gear Sets", style=discord.ButtonStyle.blurple, row=2
        )
        gear_sets_button.callback = self.gear_sets_button_callback
        gear_sets_button.disabled = True

        equip_highest_level_gear_button = Button(
            label="Equip Highest Level Gear", style=discord.ButtonStyle.green, row=2
        )
        equip_highest_level_gear_button.callback = (
            self.equip_highest_level_gear_button_callback
        )

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=3)
        back_button.callback = self.back_button_callback

        view.add_item(equipped_gear_button)
        view.add_item(armory_button)
        view.add_item(gear_sets_button)
        view.add_item(equip_highest_level_gear_button)
        view.add_item(back_button)

        return view

    def _create_armory_view(self):
        view = View(timeout=None)

        gear_type_options = [discord.SelectOption(label="All", value="all")]
        gear_type_options += [
            discord.SelectOption(label=snake_case_to_capital(g.value), value=g.value)
            for g in GearType
        ]

        gear_type_select = Select(
            placeholder="Select a gear type",
            min_values=1,
            max_values=1,
            options=gear_type_options,
            row=0,
        )
        gear_type_select.callback = self.gear_type_select_callback

        next_page_button = Button(label="⇨", style=discord.ButtonStyle.blurple, row=2)
        next_page_button.callback = self.next_page_button_callback
        if self.armory_page >= len(self.armory_pages) - 1:
            next_page_button.disabled = True

        last_page_button = Button(label="⇦", style=discord.ButtonStyle.blurple, row=2)
        last_page_button.callback = self.last_page_button_callback
        if self.armory_page == 0:
            last_page_button.disabled = True

        equipped_gear_button = Button(
            label="Equipped Gear", style=discord.ButtonStyle.blurple, row=3
        )
        equipped_gear_button.callback = self.equipped_gear_button_callback

        armory_button = Button(label="Armory", style=discord.ButtonStyle.blurple, row=3)
        armory_button.disabled = True

        gear_sets_button = Button(
            label="Gear Sets", style=discord.ButtonStyle.blurple, row=3
        )
        gear_sets_button.callback = self.gear_sets_button_callback

        equip_highest_level_gear_button = Button(
            label="Equip Highest Level Gear", style=discord.ButtonStyle.green, row=3
        )
        equip_highest_level_gear_button.callback = (
            self.equip_highest_level_gear_button_callback
        )

        back_button = Button(label="Back", style=discord.ButtonStyle.grey, row=4)
        back_button.callback = self.back_button_callback

        view.add_item(gear_type_select)
        # Add buttons to the view
        view.add_item(last_page_button)
        view.add_item(next_page_button)
        view.add_item(equipped_gear_button)
        view.add_item(armory_button)
        view.add_item(gear_sets_button)
        view.add_item(equip_highest_level_gear_button)
        view.add_item(back_button)

        return view

    @only_command_invoker()
    async def gear_select_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.view_gear_page import ViewGearPage

        await ViewGearPage(
            self.cordia_service,
            self.discord_id,
            int(interaction.data["values"][0]),
            self.gear_type == "all",
            self.armory_page,
        ).render(interaction)

    @only_command_invoker()
    async def gear_type_select_callback(self, interaction: discord.Interaction):
        if interaction.data["values"][0] == "all":
            self.armory_pages = await self.paginate_gear(None)
        else:
            self.armory_pages = await self.paginate_gear(
                GearType[interaction.data["values"][0].upper()]
            )
        self.gear_type = interaction.data["values"][0]
        self.armory_page = 0

        await self.render_armory(interaction)

    @only_command_invoker()
    async def next_page_button_callback(self, interaction: discord.Interaction):
        self.armory_page += 1
        await self.render_armory(interaction)

    @only_command_invoker()
    async def last_page_button_callback(self, interaction: discord.Interaction):
        self.armory_page -= 1
        await self.render_armory(interaction)

    @only_command_invoker()
    async def equipped_gear_button_callback(self, interaction: discord.Interaction):
        self.armory_page = -1
        await self.render(interaction)

    @only_command_invoker()
    async def armory_button_callback(self, interaction: discord.Interaction):
        self.armory_page = 0
        await self.render_armory(interaction)

    @only_command_invoker()
    async def gear_sets_button_callback(self, interaction: discord.Interaction):
        await self.render_gear_sets_view(interaction)

    @only_command_invoker()
    async def equip_highest_level_gear_button_callback(
        self, interaction: discord.Interaction
    ):
        equipped_gear = await self.cordia_service.equip_highest_level_gear(
            self.discord_id
        )
        await self.render(interaction)
        embed = discord.Embed(
            title=f"You equipped your highest level gear", color=discord.Color.green()
        )
        embed.add_field(
            name="You equipped the following gear", value="\n".join(equipped_gear)
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @only_command_invoker()
    async def back_button_callback(self, interaction: discord.Interaction):
        from cordia.view.pages.home_page import HomePage

        await HomePage(self.cordia_service, self.discord_id).render(interaction)

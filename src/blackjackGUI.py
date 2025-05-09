import discord 
from discord import Button
import UrlUtil
from jsonFormatter import formatEmbed




class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction : discord.Interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

class GameStartUI(discord.ui.View):
    @discord.ui.button(label="Button 1", row=0, style=discord.ButtonStyle.primary)
    async def click_me_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You clicked the button!")
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")
        button.disabled = True
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callbacks(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callbackss(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callbacksss(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")        

#used for hit / stand
class GameUI(discord.ui.View):
    @discord.ui.button(label="Hit", row=0, style=discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: Button):
       response = UrlUtil.hit()
       await interaction.response.edit_message(delete_after=0.01)
       msg = await interaction.channel.send(embed=formatEmbed(response.json()))
       await interaction.followup.send(view=GameUI())
    @discord.ui.button(label="Stand", row=0, style=discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: Button):
       # await interaction.response.send_message("You pressed me!")
       response = UrlUtil.stand()
       await interaction.response.edit_message(delete_after=0.01)
       await interaction.channel.send(embed=formatEmbed(response.json()))
        

    

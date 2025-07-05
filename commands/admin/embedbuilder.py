import discord
from discord.ext import commands
from discord import app_commands

class EmbedEditModal(discord.ui.Modal, title="📝 Edit Embed"):
    def __init__(self, interaction: discord.Interaction, view):
        super().__init__()
        self.interaction = interaction
        self.view = view

        self.title_input = discord.ui.TextInput(
            label="Embed Title", placeholder="Enter a title", required=False
        )
        self.description_input = discord.ui.TextInput(
            label="Embed Description", style=discord.TextStyle.paragraph,
            placeholder="Enter description text", required=False
        )
        self.image_input = discord.ui.TextInput(
            label="Image URL", placeholder="https://example.com/image.png", required=False
        )
        self.color_input = discord.ui.TextInput(
            label="Hex Color (e.g. #3498db)", placeholder="#3498db", required=False
        )

        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.image_input)
        self.add_item(self.color_input)

    async def on_submit(self, interaction: discord.Interaction):
        # Update the embed stored in the view
        embed = self.view.embed

        embed.title = self.title_input.value or discord.Embed.Empty
        embed.description = self.description_input.value or discord.Embed.Empty

        if self.image_input.value:
            embed.set_image(url=self.image_input.value)
        else:
            embed.set_image(url=None)

        if self.color_input.value:
            try:
                embed.color = discord.Color.from_str(self.color_input.value)
            except:
                embed.color = discord.Color.default()

        await interaction.response.edit_message(embed=embed, view=self.view)

class EmbedControlView(discord.ui.View):
    def __init__(self, bot, author: discord.User):
        super().__init__(timeout=300)
        self.bot = bot
        self.author = author
        self.embed = discord.Embed(
            title="AVM Embed Title",
            description="This is your preview. Click edit to customize.",
            color=discord.Color.blurple()
        )

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary, emoji="📝")
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You're not allowed to edit this.", ephemeral=True)
            return

        await interaction.response.send_modal(EmbedEditModal(interaction, self))

    @discord.ui.button(label="Send", style=discord.ButtonStyle.success, emoji="✅")
    async def send_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You're not allowed to send this.", ephemeral=True)
            return

        await interaction.channel.send(embed=self.embed)
        await interaction.response.edit_message(content="✅ Embed sent!", view=None, embed=None)

class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="embedbuilder", description="Create a custom embed interactively.")
    async def embedbuilder(self, interaction: discord.Interaction):
        view = EmbedControlView(self.bot, interaction.user)
        await interaction.response.send_message(
            content="Here's your embed preview. Customize it below:",
            embed=view.embed,
            view=view,
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(EmbedBuilder(bot))

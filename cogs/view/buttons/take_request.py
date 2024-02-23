import disnake, sqlite3

from disnake.ext import commands

from cogs.hadlers import utils
from ssbot import SSBot


def for_in_embed(in_):
    data = None
    for key_, value_ in in_:
        if key_ == "value":
            data = value_
            break

    return data


class TakeRequestButtonReg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("TakeRequestButton was added")
        self.client.add_view(TakeRequestButton(bot=self.client))


class TakeRequestButton(disnake.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, custom_id="take_request_button")
    async def take_request(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        message = await interaction.channel.fetch_message(interaction.message.id)
        client_id_from_embed = for_in_embed(in_=message.embeds[0]._fields[2].items())
        product_name_from_embed = for_in_embed(in_=message.embeds[0]._fields[0].items())
        category = disnake.utils.get(interaction.guild.categories, id=SSBot.BOT_CONFIG["requests_category_id"])
        client = interaction.guild.get_member(int(client_id_from_embed))
        avatar = utils.get_avatar(ctx_user_avatar=interaction.author.avatar)

        if interaction.author.id == client_id_from_embed:
            permissions = {
                interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False, view_channel=False),
                interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
            }
        else:
            permissions = {
                interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False, view_channel=False),
                interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True),
                client: disnake.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
            }

        channel = await interaction.guild.create_text_channel(
            name=f"{client.name}-{product_name_from_embed}",
            category=category, overwrites=permissions
        )

        embed = message.embeds[0]
        embed.set_footer(
            text=f"Запрос принял {interaction.author.display_name}",
            icon_url=avatar
        )
        await message.edit(embed=embed, view=None)

        await channel.send(f"<@{interaction.author.id}> \n<@{int(client_id_from_embed)}>")


def setup(client):
    client.add_cog(TakeRequestButtonReg(client))

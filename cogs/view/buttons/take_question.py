import disnake

from disnake.ext import commands

from cogs.hadlers import utils
from ssbot import SSBot, BOT


def for_in_embed(in_):
    data = None
    for key_, value_ in in_:
        if key_ == "value":
            data = value_
            break

    return data


class TakeQuestionButtonReg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("TakeQuestionButton was added")
        self.client.add_view(TakeQuestionButton(bot=self.client))


class TakeQuestionButton(disnake.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, custom_id="take_question_button")
    async def take_question(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        SUPPORT_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["support_channel_id"])
        message = await interaction.channel.fetch_message(interaction.message.id)
        client_id_from_embed = for_in_embed(in_=message.embeds[0]._fields[1].items())
        client = interaction.guild.get_member(int(client_id_from_embed))
        avatar = utils.get_avatar(ctx_user_avatar=interaction.author.avatar)

        embed = message.embeds[0]
        embed.set_footer(
            text=f"Вопрос принял {interaction.author.display_name}",
            icon_url=avatar
        )
        await message.edit(embed=embed, view=None)

        thread = await SUPPORT_CHANNEL.create_thread(
            name=f"Диалог с {client.display_name}",
            type=disnake.ChannelType.private_thread
        )

        await thread.send(f"<@{interaction.author.id}> <@{client.id}>")


def setup(client):
    client.add_cog(TakeQuestionButtonReg(client))

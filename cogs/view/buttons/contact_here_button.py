import disnake
from disnake.ext import commands

from ssbot import SSBot, BOT
from cogs.view.buttons.take_question import TakeQuestionButton


class ContactHereButtonReg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("TakeQuestionButton was added")
        self.client.add_view(ContactHereButton(bot=self.client))


class ContactHereButton(disnake.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Связаться здесь", style=disnake.ButtonStyle.blurple, custom_id="contact_here_button")
    async def contact_here(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        QUESTIONS_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["questions_channel_id"])

        embed_for_qc = disnake.Embed(title="Новый вопрос", color=disnake.Color.blurple())
        embed_for_qc.add_field(name=f"Имя: {interaction.author.display_name} ({interaction.author.name})", value="", inline=False)
        embed_for_qc.add_field(name="ID:", value=interaction.author.id, inline=False)

        embed = disnake.Embed(title="Уведомление отправлено", color=SSBot.DEFAULT_COLOR)
        embed.add_field(name="Я уведомил менеджеров о том, что у вас появился срочный вопрос. Скоро вам ответят.", value="")

        await QUESTIONS_CHANNEL.send(embed=embed_for_qc, view=TakeQuestionButton(self.bot))
        await interaction.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(ContactHereButtonReg(client))

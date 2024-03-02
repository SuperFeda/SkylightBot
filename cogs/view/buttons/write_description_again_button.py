import disnake, sqlite3

from disnake.ext import commands

from ssbot import SSBot


class EnterDescriptionAgainButtonReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("EnterDescriptionAgainButton was added")
        self.bot.add_view(EnterDescriptionAgainButton(bot=self.bot))


class EnterDescriptionAgainButton(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Ввести повторно", style=disnake.ButtonStyle.red, custom_id="enter_description_again_button")
    async def enter_desc_button(self, button: disnake.ui.Button, ctx):
        embed = disnake.Embed(title="Ввод описания", color=SSBot.DEFAULT_COLOR)
        embed.add_field(
            name="Напишите в чат сообщение с описанием желаемого результата. Также вы можете прикрепить исходники в количестве до 10 штук в форматах: `png`, `jpg`, `jpeg` и `gif`.",
            value="", inline=False
        )

        connection_ = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
        cursor_ = connection_.cursor()
        cursor_.execute(
            "INSERT INTO settings (user_id, can_description) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET can_description=?",
            (ctx.author.id, True, True)
        )
        connection_.commit()
        connection_.close()

        await ctx.send(embed=embed)

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(EnterDescriptionAgainButtonReg(bot))

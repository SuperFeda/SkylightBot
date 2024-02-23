import disnake
from disnake.ext import commands

from ssbot import BOT, SSBot
from cogs.view.select_menus.service_select import ServiceSelectView


class OrderMessageButtonsReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("OrderMessageButtons was added")
        self.bot.add_view(OrderMessageButtons(bot=self.bot))


class OrderMessageButtons(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(disnake.ui.Button(label="Поддержать", url="https://www.donationalerts.com/r/skylightproduction", row=1))

    @disnake.ui.button(label="Оформить заказ", style=disnake.ButtonStyle.blurple, custom_id="order_button", row=0)
    async def order_button(self, button: disnake.ui.Button, ctx: disnake.AppCmdInter):
        if SSBot.BOT_CONFIG["bot_can_take_order"] is False:
            return await ctx.send("Процесс оформления заказов временно приостановлен.", ephemeral=True)

        superfeda = BOT.get_user(875246294044643371)

        embed = disnake.Embed(title="Выбор услуги", color=disnake.Color.blurple())
        embed.add_field(
            name="Выберите желаемую услугу из списка ниже:",
            value=""
        )

        file = disnake.File("images/SkylightServices_new.png", filename="image.jpg")
        embed.set_image(url="attachment://image.jpg")
        embed.set_footer(
            text=f"{superfeda.display_name}: Вы автоматически соглашаетесь с пользовательским соглашением после оформления заказа",
            icon_url=superfeda.avatar
        )

        thread = await ctx.channel.create_thread(
            name=f"{ctx.author.name}'s заказ",
            type=disnake.ChannelType.private_thread
        )

        await thread.send(f"<@{ctx.author.id}>", embed=embed, file=file, view=ServiceSelectView(self.bot))

    @disnake.ui.button(label="Пользовательское соглашение", style=disnake.ButtonStyle.green, custom_id="ps_button", row=0)
    async def ps_button(self, button: disnake.ui.Button, ctx: disnake.AppCmdInter):
        async with ctx.channel.typing():
            await ctx.send(f'**Пользовательское соглашение** можно прочитать здесь: <#{SSBot.BOT_CONFIG["user_agreement_channel_id"]}>', ephemeral=True)

    @disnake.ui.button(label="Отзывы", style=disnake.ButtonStyle.green, custom_id="reviews_button", row=0)
    async def reviews_button(self, button: disnake.ui.Button, ctx: disnake.AppCmdInter):
        async with ctx.channel.typing():
            await ctx.send(f'**Отзывы** можно посмотреть здесь: <#{SSBot.BOT_CONFIG["feedback_channel_id"]}>', ephemeral=True)

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(OrderMessageButtonsReg(bot))

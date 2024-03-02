import disnake

from disnake.ext import commands

from ssbot import BOT, SSBot
from cogs.hadlers import utils
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
        self.support_button = disnake.ui.Button(label="Поддержать", url="https://www.donationalerts.com/r/skylightproduction", row=1)
        self.add_item(self.support_button)

    @disnake.ui.button(label="Оформить заказ", style=disnake.ButtonStyle.blurple, custom_id="order_button", row=0)
    async def order_button(self, button: disnake.ui.Button, ctx):  # ctx: disnake.AppCmdInter
        if SSBot.BOT_CONFIG["bot_can_take_order"] is False:
            return await ctx.send("Процесс оформления заказов временно приостановлен.", ephemeral=True)

        superfeda = BOT.get_user(875246294044643371)
        sf_avatar = utils.get_avatar(superfeda.avatar)

        order_embed = disnake.Embed(title="Выбор услуги", color=disnake.Color.blurple())
        order_embed.add_field(name="Выберите желаемую услугу из списка ниже:", value="")
        file = disnake.File("images/SkylightServices_new.png", filename="image.jpg")
        order_embed.set_image(url="attachment://image.jpg")
        order_embed.set_footer(
            text=f"{superfeda.display_name}: Вы автоматически соглашаетесь с пользовательским соглашением после оформления заказа",
            icon_url=sf_avatar
        )

        thread = await ctx.channel.create_thread(name=f"{ctx.author.name}'s заказ", type=disnake.ChannelType.private_thread)

        embed = utils.create_embed(title="Продолжение оформление заказа", color=SSBot.DEFAULT_COLOR, content=f"Для того чтобы продолжить оформление заказа перейдите в ветку <#{thread.id}>.")

        await thread.send(f"<@{ctx.author.id}>", embed=order_embed, file=file, view=ServiceSelectView(self.bot))
        await ctx.send(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Пользовательское соглашение", style=disnake.ButtonStyle.green, custom_id="ps_button", row=0)
    async def ps_button(self, button: disnake.ui.Button, ctx):  # ctx: disnake.AppCmdInter
        embed = utils.create_embed(title="Пользовательское соглашение", color=SSBot.DEFAULT_COLOR, content=f'**Пользовательское соглашение** можно прочитать здесь: <#{SSBot.BOT_CONFIG["user_agreement_channel_id"]}>')
        await ctx.send(embed=embed, ephemeral=True)

    @disnake.ui.button(label="Отзывы", style=disnake.ButtonStyle.green, custom_id="reviews_button", row=0)
    async def reviews_button(self, button: disnake.ui.Button, ctx):  # ctx: disnake.AppCmdInter
        embed = utils.create_embed(title="Отзывы", color=SSBot.DEFAULT_COLOR, content=f'**Отзывы** можно посмотреть здесь: <#{SSBot.BOT_CONFIG["feedback_channel_id"]}>')
        await ctx.send(embed=embed, ephemeral=True)

    # @disnake.ui.button(label="Доп. примеры работ", style=disnake.ButtonStyle.green, custom_id="work_examples_button", row=0)
    # async def reviews_button(self, button: disnake.ui.Button, ctx):  # ctx: disnake.AppCmdInter
    #         embed = utils.create_embed(title="Дополнительные примеры работ", color=SSBot.DEFAULT_COLOR, content=f'**Дополнительные примеры работ** можно посмотреть здесь: <#{SSBot.BOT_CONFIG[""]}>')
    #         await ctx.send(embed=embed, ephemeral=True)

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(OrderMessageButtonsReg(bot))

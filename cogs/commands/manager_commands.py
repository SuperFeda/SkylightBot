import disnake
from disnake.ext import commands
from disnake import Localized

from ssbot import SSBot, BOT
from cogs.hadlers import utils
from cogs.view.buttons.order_message_buttons import OrderMessageButtons
from cogs.view.select_menus.question_select import QuestionSelectView


class ManagerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="summon_order_panel")
    async def summon_order_panel(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(),  content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        ORDER_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["order_channel_id"])

        order_embed = disnake.Embed(title="Здароу, я SkylightBot", color=disnake.Color.blurple())
        order_embed.add_field(name="С моей помощью вы сможете полностью оформить заказ: выбор услуги и создание описания - со всем этим буду помогать я.\nДля начала заполнения нажмите на кнопку \"Оформить заказ\".", value="")

        await ORDER_CHANNEL.send(embed=order_embed, view=OrderMessageButtons(self.bot))

    @commands.slash_command(name="summon_support_panel")
    async def summon_support_panel(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(), content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        SUPPORT_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["support_channel_id"])

        support_embed = disnake.Embed(title="Поддержка", color=disnake.Color.blurple())
        support_embed.add_field(name="Тут я попытаюсь ответить на все вопросы, которые могли появится у вас во время работы с сервисом.\nВыберите интересующую вас тему в списке ниже:", value="")

        await SUPPORT_CHANNEL.send(embed=support_embed, view=QuestionSelectView(self.bot))

    @commands.slash_command(name="clear_services_list")
    async def clear_services_list(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(),  content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="update_services_list")
    async def update_services_list(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(),  content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        async with ctx.channel.typing():
            SERVICES_CHANNEL = BOT.get_channel(1211977678023036958)  # test services channel
            # SERVICES_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["services_channel_id"])
            # applied_tags=["Логотип"],

            # Создание страницы с услугой "Буквенный логотип"
            icon = disnake.File("images/services_icons/logo_icon.png", filename="logo_icon.jpg")
            embed = disnake.Embed(title="Буквенный логотип", color=disnake.Color.blurple())
            embed.add_field(name="**Цена: 249₽**\n\nОтличная вещь для оформления сервера или страницы скачивания мода.\n\n:arrow_down: Примеры работ ниже :arrow_down:", value=f'\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>', inline=False)
            embed.set_image(url="attachment://logo_icon.jpg")

            LETTER_LOGO_MESSAGE = await SERVICES_CHANNEL.create_thread(name="Буквенный логотип", embed=embed, file=icon)
            LETTER_LOGO_THREAD = BOT.get_channel(LETTER_LOGO_MESSAGE.thread.id)

            await LETTER_LOGO_THREAD.send(file=disnake.File("images/services_work_examples/logo_example.png"))

            # Создание страницы с услугой "Скин 64х64"
            icon = disnake.File("images/services_icons/skin_icon.png", filename="skin_icon.jpg")
            embed = disnake.Embed(title="Буквенный логотип", color=disnake.Color.blurple())
            embed.add_field(name="**Цена: 280₽**\n\nНадоели обычные Стив и Алекс? Новые скины тоже успели надоесть? Тогда мы поможем вам создать уникальный дизайн для вашего скина.\n\n:arrow_down: Примеры работ ниже :arrow_down:", value=f'\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>', inline=False)
            embed.set_image(url="attachment://skin_icon.jpg")

            SKIN_MESSAGE = await SERVICES_CHANNEL.create_thread(name="Скин 64х64", embed=embed, file=icon)
            SKIN_THREAD = BOT.get_channel(SKIN_MESSAGE.thread.id)

            await SKIN_THREAD.send(file=disnake.File("images/services_work_examples/skins_example.png"))
            
            # InteractionTimedOut: Interaction took more than 3 seconds to be responded to. Please defer it using "interaction.response.defer" on the start of your command. Later you may send a response by editing the deferred message using "interaction.edit_original_response"
            # Note: This might also be caused by a misconfiguration in the components make sure you do not respond twice in case this is a component.

        await ctx.send("b", ephemeral=True)


def setup(bot):
    bot.add_cog(ManagerCommands(bot))

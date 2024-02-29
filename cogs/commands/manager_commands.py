import disnake

from disnake.ext import commands
from disnake import Localized
from typing import List

from ssbot import SSBot, BOT
from cogs.hadlers import utils, dicts
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

        SERVICES_CHANNEL = BOT.get_channel(1211977678023036958)

    @commands.slash_command(name="update_services_list")
    async def update_services_list(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(),  content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        await ctx.response.defer(ephemeral=True)

        SERVICES_CHANNEL = BOT.get_channel(1211977678023036958)  # test services channel
        # SERVICES_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["services_channel_id"])
        # applied_tags=["Логотип"],

        # Создание страницы с услугой "Буквенный логотип"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Буквенный логотип",
            icon_path="images/services_icons/logo_icon.png",
            icon_name="logo_icon.jpg",
            embed_title="Буквенный логотип",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.LETTER_LOGO]}₽\n\nОтличная вещь для оформления сервера или страницы скачивания мода.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/logo_example.png")]
        )

        # Создание страницы с услугой "Скин 64х64"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Скин 64х64",
            icon_path="images/services_icons/skin_icon.png",
            icon_name="skin_icon.jpg",
            embed_title="Скин 64х64",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.SKIN64]}₽\n\nНадоели обычные Стив и Алекс? Новые скины тоже успели надоесть? Тогда мы поможем вам создать уникальный дизайн для вашего скина.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/skins_example.png")]
        )

        await ctx.edit_original_message("test")

    async def create_service_post(self, *, service_channel: disnake.ForumChannel, thread_name: str, icon_path: str,
                                  icon_name: str, embed_title: str, embed_field_name: str, embed_field_value: str,
                                  examples: list[disnake.File]) -> None:
        icon = disnake.File(icon_path, filename=icon_name)
        embed = disnake.Embed(title=embed_title, color=disnake.Color.blurple())
        embed.add_field(name=embed_field_name, value=embed_field_value, inline=False)
        embed.set_image(url=f"attachment://{icon_name}")

        THREAD_MESSAGE = await service_channel.create_thread(name=thread_name, embed=embed, file=icon)
        THREAD = BOT.get_channel(THREAD_MESSAGE.thread.id)

        await THREAD.send("Примеры работ:", files=examples)


def setup(bot):
    bot.add_cog(ManagerCommands(bot))

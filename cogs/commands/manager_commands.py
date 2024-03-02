import disnake

from disnake.ext import commands

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

    # @commands.slash_command(name="clear_services_list")
    # async def clear_services_list(self, ctx):
    #     if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
    #         embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(),  content="У вас нет прав на использование этой команды.")
    #         return await ctx.send(embed=embed, ephemeral=True)
    #
    #     SERVICES_CHANNEL = BOT.get_channel(1211977678023036958)

    @commands.slash_command(name="update_services_list")
    async def update_services_list(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["manager_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(),  content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        await ctx.response.defer(ephemeral=True)

        SERVICES_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["services_channel_id"])

        # Создание страницы с услугой "Плащ"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Плащ",
            tag=SERVICES_CHANNEL.get_tag_by_name("Скин"),
            icon_path="images/services_icons/cape_icon.jpg",
            icon_name="cape_icon.jpg",
            embed_title="Плащ",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.CAPE]}₽\n\nИнтересный вариант для того, чтобы разнообразить ваш скин.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/cape_example.jpg")]
        )

        # Создание страницы с услугой "Текстура для блока/предмета"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Текстура для блока/предмета",
            tag=SERVICES_CHANNEL.get_tag_by_name("Текстура"),
            icon_path="images/services_icons/texture_icon.png",
            icon_name="texture_icon.jpg",
            embed_title="Текстура для блока/предмета",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.TEXTURE]}₽\n\nТекстура - основное составляющее всего визуала Minecraft. Мы реализуем любые идеи для модов, ресурс-паков и не только, для улучшения того самого визуала.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/texture_example_2.jpg"), disnake.File("images/services_work_examples/texture_example.png")]
        )

        # Создание страницы с услугой "Дизайн персонажей"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Дизайн персонажей",
            tag=SERVICES_CHANNEL.get_tag_by_name("Специально"),
            icon_path="images/services_icons/characters_design_icon.png",
            icon_name="characters_design_icon.jpg",
            embed_title="Дизайн персонажей",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.CHARACTERS_DESIGN]}₽\n\nРисовка персонажей в уникальном стиле, которых можно использовать в создании анимации или любых других целей.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/characters_design_example.png")]
        )

        # Создание страницы с услугой "Тотем"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Тотем",
            tag=SERVICES_CHANNEL.get_tag_by_name("Текстура"),
            icon_path="images/services_icons/totem_icon.png",
            icon_name="totem_icon.jpg",
            embed_title="Тотем",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.TOTEM]}₽\n\nХотите ли вы, чтобы тотем сохраняющий вашу жизнь, был похож на вас или вашего товарища? Тогда мы поможем в реализации вашей идеи!\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/totem_example.png")]
        )

        # Создание страницы с услугой "Скин 64х64"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Скин 64х64",
            tag=SERVICES_CHANNEL.get_tag_by_name("Скин"),
            icon_path="images/services_icons/skin_icon.png",
            icon_name="skin_icon.jpg",
            embed_title="Скин 64х64",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.SKIN64]}₽\n\nНадоели обычные Стив и Алекс? Новые скины тоже успели надоесть? Тогда мы поможем вам создать уникальный дизайн для вашего скина.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/skins_example.png")]
        )

        # Создание страницы с услугой "Модель"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Модель",
            tag=SERVICES_CHANNEL.get_tag_by_name("Модель"),
            icon_path="images/services_icons/model_icon.jpg",
            icon_name="model_icon.jpg",
            embed_title="Модель",
            embed_field_name=f'**Цена только модели: от {dicts.NOT_STATIC_PRICE[SSBot.MODEL]}₽**\n**Цена модели + текстура: от {dicts.NOT_STATIC_PRICE[SSBot.TEXTURE_MODEL]}₽**\n**Цена модели + анимация: от {dicts.NOT_STATIC_PRICE[SSBot.ANIM_MODEL]}₽**\n\nМодель - один из главных элементов любого мода, способный показать весь визуал модификации.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/model_example.jpg"), disnake.File("images/services_work_examples/model_example_2.png"), disnake.File("images/services_work_examples/model_animation_example.gif")]
        )

        # Создание страницы с услугой "Буквенный логотип"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Буквенный логотип",
            tag=SERVICES_CHANNEL.get_tag_by_name("Логотип"),
            icon_path="images/services_icons/logo_icon.png",
            icon_name="logo_icon.jpg",
            embed_title="Буквенный логотип",
            embed_field_name=f'Цена: {dicts.SERVICE_PRICES[SSBot.LETTER_LOGO]}₽\n\nОтличная вещь для оформления сервера или страницы скачивания мода.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/logo_example.png")]
        )

        # Создание страницы с услугой "Буквенный логотип с кастомными буквами/доп. деталями"
        await self.create_service_post(
            service_channel=SERVICES_CHANNEL,
            thread_name="Буквенный логотип с кастомными буквами/доп. деталями",
            tag=SERVICES_CHANNEL.get_tag_by_name("Логотип"),
            icon_path="images/services_icons/logo2_icon.png",
            icon_name="logo2_icon.jpg",
            embed_title="Буквенный логотип с кастомными буквами/доп. деталями",
            embed_field_name=f'Цена: от {dicts.NOT_STATIC_PRICE[SSBot.LETTER_LOGO_2]}₽\n\nОтличная вещь для оформления сервера или страницы скачивания мода.\n\n(Оформить заказ можно здесь: <#{SSBot.BOT_CONFIG["order_channel_id"]}>) ',
            embed_field_value=':arrow_down::arrow_down: ***Примеры работ ниже*** :arrow_down::arrow_down:',
            examples=[disnake.File("images/services_work_examples/logo2_examples.png")]
        )

        await ctx.edit_original_message("Список услуг обновлен.")

    async def create_service_post(self, *, service_channel: disnake.ForumChannel, thread_name: str, icon_path: str,
                                  tag: disnake.ForumTag, icon_name: str, embed_title: str, embed_field_name: str,
                                  embed_field_value: str, examples: list[disnake.File]) -> None:
        icon = disnake.File(icon_path, filename=icon_name)
        embed = disnake.Embed(title=embed_title, color=disnake.Color.blurple())
        embed.add_field(name=embed_field_name, value=embed_field_value, inline=False)
        embed.set_image(url=f"attachment://{icon_name}")

        THREAD_MESSAGE = await service_channel.create_thread(applied_tags=[tag], name=thread_name, embed=embed, file=icon)
        THREAD = BOT.get_channel(THREAD_MESSAGE.thread.id)

        await THREAD.send("Примеры работ:", files=examples)


def setup(bot):
    bot.add_cog(ManagerCommands(bot))

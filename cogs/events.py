import disnake, sqlite3, os
from disnake.ext import commands
from colorama import Fore

from ssbot import BOT, SSBot
from cogs.hadlers import utils
from cogs.view.select_menus.question_select import QuestionSelectView
from cogs.view.buttons.write_description_again_button import EnterDescriptionAgainButton
from cogs.view.buttons.order_message_buttons import OrderMessageButtons
from cogs.view.buttons.continue_and_adtcon_buttons import ContinueAndAdtConButtons


class BotEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # отправка сообщения, через которое происходит оформление заказа в канал ORDER_CHANNEL, как только бот становится активен
        print(f"{Fore.RED}[WARN]{Fore.RESET} Бот запущен и готов начать самую большую оргию")

        ORDER_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["order_channel_id"])
        SUPPORT_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["support_channel_id"])

        order_embed = disnake.Embed(title="Здароу, я SkylightBot", color=disnake.Color.blurple())
        order_embed.add_field(name="С моей помощью вы сможете полностью оформить заказ: выбор услуги и создание описания - со всем этим буду помогать я.\nДля начала заполнения нажмите на кнопку \"Оформить заказ\".", value="")

        support_embed = disnake.Embed(title="Поддержка", color=disnake.Color.blurple())
        support_embed.add_field(name="Тут я попытаюсь ответить на все вопросы, которые могли появится у вас во время работы с сервисом.\nВыберите интересующую вас тему в списке ниже:", value="")

        # await SUPPORT_CHANNEL.send(embed=support_embed, view=QuestionSelectView(self.client))
        # await ORDER_CHANNEL.send(embed=order_embed, view=OrderMessageButtons(self.client))

    @commands.Cog.listener()
    async def on_message(self, message):
        connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
        cursor = connection.cursor()
        cursor.execute("SELECT can_description FROM settings WHERE user_id=?", (message.author.id,))
        result = cursor.fetchone()
        can_description_var = result[0] if result else None
        connection.close()

        if message.channel.type is disnake.ChannelType.private_thread and message.author.name in message.channel.name:
            def is_not_bot(m):
                return not m.author.bot
            await message.channel.purge(check=is_not_bot)  # Удаление сообщений в новосозданной ветке

        if can_description_var == 1 or can_description_var is True:
            pictures = None
            embed_for_send = []

            connection_ = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
            cursor_ = connection_.cursor()
            cursor_.execute(
                "INSERT INTO settings (user_id, service_description) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET service_description=?",
                (message.author.id, message.content, message.content)
            )
            connection_.commit()
            connection_.close()

            if len(message.attachments) > 10:
                embed = utils.create_embed(title="Слишком много изображений", color=disnake.Color.red(), content="Отправить можно максимум 10 изображений.")
                return await message.channel.send(f"<@{message.author.id}>", embed=embed, delete_after=12)
            if len(message.content) > 1020:
                embed = utils.create_embed(title="Слишком длинное описание", color=disnake.Color.red(), content="Описание должно вмещать в себя до **1020** символов.")
                return await message.channel.send(f"<@{message.author.id}>", embed=embed, delete_after=12)

            async with message.channel.typing():
                if message.author.name in os.listdir("cache/"):  # если папка с именем пользователя уже есть в папке с кешем, то удалить ее и ее содержимое
                    utils.delete_files_from_cache(author_name=message.author.name)

                desc = disnake.Embed(title="Проверка описания", color=SSBot.DEFAULT_COLOR)
                desc.add_field(
                    name=f"Проверьте введенное вами описание и прикрепленные фотографии (при наличии):",
                    value=f"**{message.content}**", inline=False
                )
                desc.add_field(
                    name="При наличиии ошибок в тексте или если забыли что-то дописать, то нажмите на кнопку \"Ввести повторно\".\n\nЕсли вы можете предоставить дополнительные контакты для связи то нажмите на кнопку \"Доп. контакты\"",
                    value="", inline=False
                )
                embed_for_send.append(desc)

                if len(message.attachments) > 0:
                    banned_filenames = []
                    for image in message.attachments:
                        img_fln = image.filename[-5:]
                        # если файл имеет не разрешенный формат, то добавить его имя в список "banned_filenames"
                        if ".png" not in img_fln and ".jpeg" not in img_fln and ".gif" not in img_fln and ".jpg" not in img_fln:
                            banned_filenames.append(image.filename)
                        else:
                            try:
                                os.mkdir(f"cache/{message.author.name}/")  # создание папки с именем пользователя в кеше
                            except FileExistsError:
                                pass
                            await image.save(f"cache/{message.author.name}/{image.filename}")

                    if banned_filenames:
                        banned_files_embed = disnake.Embed(
                            title="Файлы заблокированы",
                            description="**Список заблокированных файлов из-за не поддерживаемого формата:** {}".format(", ".join(banned_filenames)),
                            color=disnake.Color.red()
                        )
                        embed_for_send.append(banned_files_embed)

                    warning_message = disnake.Embed(title="Уведомление", color=SSBot.DEFAULT_COLOR)
                    warning_message.add_field(
                        name="Если я отправил не все изображения, что вы прикрепляли, то возможно это произошло из-за того, что ваши изображения имеют одинаковое название либо не разрешенный формат.",
                        value="", inline=False
                    )
                    warning_message.add_field(
                        name="Пожалуйста, перепроверьте эти факторы и повторно отправьте изображения.\nСписок поддерживаемый форматов файлов: `png`, `jpg`, `jpeg` и `gif`",
                        value="", inline=False
                    )
                    embed_for_send.append(warning_message)

                    pictures = utils.get_files(f"cache/{message.author.name}/")  # получение сохраненных фотографий из кеша

            connection_ = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
            cursor_ = connection_.cursor()
            cursor_.execute(
                "INSERT INTO settings (user_id, can_description) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET can_description=?",
                (message.author.id, False, False)
            )
            connection_.commit()
            connection_.close()

            components_list = [
                EnterDescriptionAgainButton(self.client).enter_desc_button,
                ContinueAndAdtConButtons(self.client).continue_button,
                ContinueAndAdtConButtons(self.client).additional_contacts_button
            ]

            await message.channel.send(embeds=embed_for_send, files=pictures, components=components_list)

        LOG_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["log_channel_id"])

        if message.author != BOT.user:                                        # отправка сообщений от всех пользователей в LOG_CHANNEL, если id канала, где
            if message.channel.id in SSBot.BOT_CONFIG["banned_channels_id"]:  # было опубликованно сообщение не находится в banned_channels и автор сообщения не SSBot
                return
            avatar = utils.get_avatar(ctx_user_avatar=message.author.avatar.url)

            embed = disnake.Embed(title="Сообщение", color=SSBot.DEFAULT_COLOR)
            embed.add_field(name=f'"<#{message.channel.id}>" :>> ', value=message.content)
            embed.set_author(name=message.author.display_name, icon_url=avatar)
            try:
                await LOG_CHANNEL.send(embed=embed)
            except disnake.errors.HTTPException:
                await LOG_CHANNEL.send(f"В <#{message.channel.id}> было отправлено сообщение длинной больше 1024 символов от {message.author.display_name} ({message.author.name})")

        await BOT.process_commands(message)


def setup(client):
    client.add_cog(BotEvents(client))

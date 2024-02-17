import disnake, sqlite3, os, shutil
from disnake.ext import commands
from colorama import Fore

from ssbot import BOT, SSBot
from cogs.hadlers import handlers
from cogs.view.service_select import ServiceSelectView
# from cogs.view.buttons.continue_button import ContinueButton
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

        embed = disnake.Embed(title="Здароу, я SkylightBot", color=disnake.Color.blurple())
        embed.add_field(name="С моей помощью вы сможете полностью оформить заказ: выбор услуги и описание - со всем этим буду помогать я.\nДля начала заполнения нажмите на кнопку \"Оформить заказ\".", value="")
        await ORDER_CHANNEL.send(embed=embed, view=OrderMessageButtons(self.client))

    @commands.Cog.listener()
    async def on_message(self, message):
        pictures = None

        if message.channel.type is disnake.ChannelType.private_thread and message.author.name in message.channel.name:
            connection_ = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
            cursor_ = connection_.cursor()
            cursor_.execute(
                "INSERT INTO settings (user_id, service_description) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET service_description=?",
                (message.author.id, message.content, message.content)
            )
            connection_.commit()
            connection_.close()

            def is_not_bot(m):
                return not m.author.bot
            await message.channel.purge(check=is_not_bot)

            if len(message.attachments) > 10:
                return await message.send("Отправить можно максимум 10 изображений.", delete_after=2)
            if len(message.content) > 349:
                return await message.send("Описание должно вмещать в себя до **349** символов.", delete_after=2)

            async with message.channel.typing():
                if message.author.name in os.listdir("cache/"):
                    for file in os.listdir(f"cache/{message.author.name}/"):
                        os.remove(f"cache/{message.author.name}/{file}")
                    os.rmdir(f"cache/{message.author.name}")

                if len(message.attachments) > 0:
                    for image in message.attachments:
                        img_fln = image.filename[-5:]
                        if ".png" not in img_fln and ".jpeg" not in img_fln and ".gif" not in img_fln and ".jpg" not in img_fln:
                            pass
                        else:
                            try:
                                os.mkdir(f"cache/{message.author.name}/")
                            except FileExistsError:
                                pass
                            await image.save(f"cache/{message.author.name}/{image.filename}")

                    pictures = handlers.get_files(f"cache/{message.author.name}/")

                    # picture_for_send = []
                    # for image_for_send in os.listdir(f"cache/{message.author.name}/"):
                    #     picture_for_send.append(disnake.File(f"cache/{message.author.name}/{image_for_send}"))

                embed = disnake.Embed(title="Проверка описания", color=SSBot.DEFAULT_COLOR)
                embed.add_field(
                    name=f"Проверьте введенное вами описание и прикрепленные фотографии (при наличии): **{message.content}**",
                    value="",
                    inline=False
                )
                embed.add_field(
                    name="Если вы можете предоставить дополнительные контакты для связи то нажмите на кнопку \"Доп. контакты\"",
                    value="",
                    inline=False
                )

            await message.channel.send(embed=embed, files=pictures, view=ContinueAndAdtConButtons(self.client))

        BANNED_CHANNELS = [
            1169299255597469696, 1130088587661148290, 1130088521718300682,
            1130087805553475634, 1130091204546150441, 1130091606620524554,
            1130092027942555740, 1130498251167105085, 1130108061550399518,
            1130521980936921200, 1130087595993468979, 1130086029743890516,
            1130091118760034385, 1130090840145022977, 1130086029743890517
        ]  # список каналов из которых не нужно записывать логи (сообщения юзеров)
        LOG_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["log_channel_id"])

        if message.author != BOT.user:                 # отправка сообщений от всех пользователей в LOG_CHANNEL, если id канала, где
            if message.channel.id in BANNED_CHANNELS:  # было опубликованно сообщение не находится в banned_channels и автор сообщения не бот
                return
            embed = disnake.Embed(title="Сообщение")
            embed.add_field(name=f'"**{message.channel.name}**" :>> {message.content}.', value="")
            if not message.author.avatar:
                embed.set_author(name=message.author.display_name)
            else:
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
            await LOG_CHANNEL.send(embed=embed)

        await BOT.process_commands(message)


def setup(client):
    client.add_cog(BotEvents(client))

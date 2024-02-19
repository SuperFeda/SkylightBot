import disnake, sqlite3
from disnake.ext import commands
from disnake import Localized

from ssbot import BOT
from cogs.hadlers import bot_choices, utils
# from cogs.view.buttons.continue_button import ContinueButton
from cogs.view.buttons.take_request import TakeRequestButton


class ClientCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name=Localized("send_report", key="send_report.display_name"),
        description=Localized("Notify employees about an error in the service", key="send_report.description"),
        options=[
            disnake.Option(name=Localized("message", key="send_report.message.name"), description=Localized("Your message:", key="send_report.message.description"), required=True),
            disnake.Option(name=Localized("report_type", key="send_report.report_type.name"), description=Localized("Select report type:", key="send_report.report_type.description"), choices=bot_choices.CHOICE_FOR_REPORT_TYPE, required=True)
        ]
    )
    async def send_report(self, ctx, message: str, report_type: str):
        REPORT_CHANNEL = BOT.get_channel(BOT.BOT_CONFIG["report_channel_id"])

        await ctx.send("Репорт отправлен", ephemeral=True)

        embed = disnake.Embed(title="Репорт:")
        embed.add_field(name=f"Тип репорта: {report_type}", value="", inline=False)
        embed.add_field(name=f"Сообщение: {message}", value='', inline=False)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)

        await REPORT_CHANNEL.send(embed=embed)

    # @commands.slash_command(
    #     name=Localized("additional_contacts", key="additional_contacts.display_name"),
    #     description=Localized("Provide additional contacts to contact you", key="additional_contacts.description"),
    #     options=[
    #         disnake.Option(name=Localized("email_address", key="additional_contacts.email_address"), required=False),
    #         disnake.Option(name=Localized("telegram_url", key="additional_contacts.telegram_url"), required=False),
    #         disnake.Option(name=Localized("vk_url", key="additional_contacts.vk_url"), required=False)
    #     ]
    # )
    # async def additional_contacts(self, ctx, email_address: str | None = None, telegram_url: str | None = None, vk_url: str | None = None):
    #     connection = sqlite3.connect(BOT.PATH_TO_CLIENT_DB)
    #     cursor = connection.cursor()
    #     user_id = ctx.author.id
    #     cursor.execute(
    #         "INSERT INTO settings (user_id, mail, telegram_url, vk_url) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET mail=?, telegram_url=?, vk_url=?",
    #         (user_id, email_address, telegram_url, vk_url, email_address, telegram_url, vk_url)
    #     )
    #     connection.commit()
    #     connection.close()
    #
    #     embed = disnake.Embed(title="Предоставленные контакты:")
    #
    #     if vk_url is not None:
    #         embed.add_field(name=f'VK: {vk_url}', value="")
    #     if email_address is not None:
    #         embed.add_field(name=f'Email: {email_address}', value="")
    #     if telegram_url is not None:
    #         embed.add_field(name=f'Telegram: {telegram_url}', value="")
    #
    #     await ctx.send(embed=embed, ephemeral=True, view=ContinueButton(self.bot))

    # @commands.slash_command(
    #     name=Localized("description", key="description.display_name"),
    #     description=Localized("Describe the implementation of the order", key="description.description"),
    #     options=[
    #         disnake.Option(name=Localized("description", key="description.description.name"), description=Localized("Write here: how you want to see the order total", key="description.description.description"), required=True),
    #         disnake.Option(name=Localized("images", key="description.images.name"), description=Localized("Leave here a link to the images based on which you need to complete the order, if available", key="description.images.description"), required=False)
    #     ]
    # )
    # async def description(self, ctx, description: str, images: str | None = None):
    #     connection = sqlite3.connect(BOT.PATH_TO_CLIENT_DB)
    #     cursor = connection.cursor()
    #     user_id = ctx.author.id
    #     cursor.execute(
    #         "INSERT INTO settings (user_id, service_description, service_images) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET service_description=?, service_images=?",
    #         (user_id, description, images, description, images)
    #     )
    #     connection.commit()
    #     connection.close()
    #
    #     if len(description) > 800:
    #         return await ctx.send("Ошибка. Описание должно содержать максимум 800 символов.", ephemeral=True)
    #
    #     if images is None:
    #         pass
    #     elif "https://mega.nz/" not in images and "https://drive.google.com/" not in images and "https://disk.yandex.ru/" not in images and "https://imgur.com/" not in images:
    #         # elif images not in ["https://mega.nz/", "https://drive.google.com/", "https://disk.yandex.ru/"]:
    #         return await ctx.send(
    #             "Этого сайта нет в белом списке SkylightServices. Пожалуйста, выберите одино из этих облоков и загрузите фотографии туда:\n1) https://mega.nz/ \n2) https://drive.google.com/ \n3) https://disk.yandex.ru/ \n4) https://imgur.com/",
    #             ephemeral=True, suppress_embeds=True
    #         )
    #
    #     await ctx.send(
    #         f'Проверьте: всё ли правильно написано, если нет, то снова введите команду `/описание` (`/description`).\nСсылка на фотографии: {images}\nВаш текст: {description}\n\nЕсли вы можете предоставить дополнительные контакты для связи с вами, то воспользуйтесь командой `/дополнительные_контакты` (`/additional_contacts`) и выберите подходящие варианты.',
    #         view=ContinueButton(self.bot), ephemeral=True
    #     )

    @commands.slash_command(
        name=Localized("archive", key="archive.display_name"),
        description=Localized("Send a request to purchase an item from the archive or an offer to add it", key="archive.description"),
        options=[
            disnake.Option(name=Localized("product_name", key="archive.product_name.name"), description=Localized("The name of the desired product:", key="archive.product_name.description"), required=True),
            disnake.Option(name=Localized("request_type", key="archive.request_type.name"), description=Localized("Select which type your enquiry belongs to:", key="archive.request_type.description"), choices=bot_choices.CHOICE_FOR_REQUEST_TYPE, required=True)
        ]
    )
    async def archive(self, ctx, product_name: str, request_type: str):
        color = utils.color_archive_request(request_type)
        channel = BOT.get_channel(BOT.BOT_CONFIG["request_channel_id"])

        embed = disnake.Embed(title="Новый запрос:", color=color)
        embed.add_field(name="Имя продукта:", value=product_name, inline=False)
        embed.add_field(name="Тип запроса:", value=request_type, inline=False)
        embed.add_field(name="ID запрашивающего:", value=ctx.author.id, inline=False)
        embed.set_author(name=f"{ctx.author.display_name} // {ctx.author.name}", icon_url=ctx.author.avatar)

        await ctx.send("Ваш запрос отправлен.", ephemeral=True)
        await channel.send(embed=embed, view=TakeRequestButton(bot=self.bot))

    # @commands.slash_command(
    #     name=Localized("place_an_order", key="place_an_order.name"),
    #     description=Localized("Command to place an order in any channel", key="place_an_order.description")
    # )
    # async def place_an_order(self, ctx):
    #     embed = disnake.Embed(title="SkylightServices", color=disnake.Color.blurple())
    #     embed.add_field(
    #         name="Посмотреть список услуг: <#1130088587661148290>\nОтзывы: <#1130088521718300682>\n\n**Перед оформлением заказа не забудьте прочитать пользовательское соглашение в канале** <#1169299255597469696>",
    #         value=""
    #     )
    #
    #     superfeda = BOT.get_user(875246294044643371)
    #
    #     file = disnake.File("SkylightServices_new.png", filename="image.jpg")
    #     embed.set_image(url="attachment://image.jpg")
    #     embed.set_footer(
    #         text=f"{superfeda.display_name}: Вы автоматически соглашаетесь с пользовательским соглашением после оформления заказа",
    #         icon_url=superfeda.avatar
    #     )
    #
    #     await ctx.send(embed=embed, file=file, ephemeral=True, view=ServiceSelectView(self.bot))


def setup(bot):
    bot.add_cog(ClientCommands(bot))

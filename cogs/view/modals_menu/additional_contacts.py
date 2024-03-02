import disnake, sqlite3

from disnake.ext import commands

from ssbot import SSBot


# Класс для регистрации этого файла как кога, чтобы его можно было загрузить в main
class AdditionalContactsMenuReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("AdditionalContactsMenu was added")
        self.bot.add_view(AdditionalContactsMenu(bot=self.bot))


class AdditionalContactsMenu(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            title="Ввод дополнительных контактов связи", custom_id="additional_contacts_menu",
            timeout=450.0, components=[
                disnake.ui.TextInput(
                    label="Ссылка на VK",
                    placeholder="vk.com/example",
                    custom_id="vk_url",
                    required=False,
                    style=disnake.TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Ссылка на Telegram",
                    placeholder="@example",
                    custom_id="tg_url",
                    required=False,
                    style=disnake.TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Адрес электронной почты",
                    placeholder="example@mail.ru",
                    custom_id="mail_address",
                    required=False,
                    style=disnake.TextInputStyle.short,
                    max_length=60,
                )
            ]
        )

    async def callback(self, ctx):
        from cogs.view.buttons.continue_and_adtcon_buttons import ContinueAndAdtConButtons

        async with ctx.channel.typing():
            vk_url_from_mm = ctx.text_values["vk_url"]               # Получение данных
            tg_url_from_mm = ctx.text_values["tg_url"]               # из TextInput
            mail_address_from_mm = ctx.text_values["mail_address"]   # из AdditionalContactsMenu

            embed = disnake.Embed(title="Доп. контакты", color=SSBot.DEFAULT_COLOR)
            embed.add_field(name="Проверьте, все ли данные введены верно:", value="")

            if vk_url_from_mm != "":
                embed.add_field(name=f'VK: {vk_url_from_mm}', value="", inline=False)
            if tg_url_from_mm != "":
                embed.add_field(name=f'Telegram: {tg_url_from_mm}', value="", inline=False)
            if mail_address_from_mm != "":
                embed.add_field(name=f'Электронная почта: {mail_address_from_mm}', value="", inline=False)

            embed.add_field(
                name="Если где-то имеется ошибка, то повторно нажмите на кнопку \"Доп. контакты\".",
                value="",
                inline=False
            )

            connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO settings (user_id, vk_url, mail, telegram_url) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET vk_url=?, mail=?, telegram_url=?",
                (ctx.author.id, vk_url_from_mm, mail_address_from_mm, tg_url_from_mm, vk_url_from_mm, mail_address_from_mm, tg_url_from_mm)
            )
            connection.commit()
            connection.close()

        await ctx.send(embed=embed, view=ContinueAndAdtConButtons(self.bot))


def setup(bot):
    bot.add_cog(AdditionalContactsMenuReg(bot))

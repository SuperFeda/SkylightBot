import disnake, sqlite3

from disnake.ext import commands

from ssbot import SSBot
from cogs.hadlers import utils
from cogs.view.buttons.donation_and_promo_code_buttons import DonationAndPromoCodeButtons
from cogs.view.modals_menu.additional_contacts import AdditionalContactsMenu


class ContinueAndAdtConButtonsReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ContinueAndAdtConButtons was added")
        self.bot.add_view(ContinueAndAdtConButtons(bot=self.bot))


class ContinueAndAdtConButtons(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Продолжить", style=disnake.ButtonStyle.green, custom_id="continue_button")
    async def continue_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
        cursor = connection.cursor()
        user_id = interaction.author.id

        # find client name
        cursor.execute("SELECT client_name FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_name = result[0] if result else None

        # find client avatar
        cursor.execute("SELECT client_avatar FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_avatar = result[0] if result else None

        # find client display name
        cursor.execute("SELECT client_display_name FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_display_name = result[0] if result else None

        # find service type
        cursor.execute("SELECT service_type FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_type = result[0] if result else None

        # find service description
        cursor.execute("SELECT service_description FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_description = result[0] if result else None

        # find service code
        cursor.execute("SELECT service_code FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_code = result[0] if result else None

        # find sending time
        cursor.execute("SELECT sending_time FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_sending_time = result[0] if result else None

        # find vk
        cursor.execute("SELECT vk_url FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_vk_url = result[0] if result else None

        # find mail
        cursor.execute("SELECT mail FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_mail = result[0] if result else None

        # find telegram url
        cursor.execute("SELECT telegram_url FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_telegram_url = result[0] if result else None

        connection.close()

        color = utils.color_order(var_service_type)

        order_embed = disnake.Embed(title='Ваш заказ:', color=color)
        order_embed.add_field(name=f'Код заказа: {var_service_code}\nДата оформления: {var_sending_time} (МСК / GMT+3)\nИмя заказчика: {var_client_display_name} (tag: {var_client_name})\nУслуга: {var_service_type}', value="")
        order_embed.add_field(name="Описание:", value=var_service_description, inline=False)

        if var_mail != "" and var_mail is not None or var_vk_url != "" and var_vk_url is not None or var_telegram_url != "" and var_telegram_url is not None:
            order_embed.add_field(name="Доп. контакты связи:", value="", inline=False)
            if var_vk_url != "" and var_vk_url is not None:
                order_embed.add_field(name=f'VK: {var_vk_url}', value="", inline=False)
            if var_mail != "" and var_mail is not None:
                order_embed.add_field(name=f'Электронная почта: {var_mail}', value="", inline=False)
            if var_telegram_url != "" and var_telegram_url is not None:
                order_embed.add_field(name=f'Telegram: {var_telegram_url}', value="", inline=False)

        if not interaction.author.avatar or interaction.author.avatar is None:
            order_embed.set_author(name=var_client_display_name)
        else:
            order_embed.set_author(name=var_client_display_name, icon_url=var_client_avatar)

        embed = disnake.Embed(title="Проверка содержимого заказа", color=disnake.Color.blurple())
        embed.add_field(name="Проверьте данные и запомните код заказа.\n**В тексте доната *ОБЯЗАТЕЛЬНО* напишите ваш Discord ник и код заказа, в ином случае заказ не будет выполнен.**", value="", inline=False)

        button_list = [
            DonationAndPromoCodeButtons(self.bot).pay_button,
            DonationAndPromoCodeButtons(self.bot).promo_code_button
        ]

        try:
            pictures = utils.get_files(f"cache/{interaction.author.name}/")
            await interaction.response.send_message(embeds=[embed, order_embed], files=pictures, view=DonationAndPromoCodeButtons(self.bot))
        except FileNotFoundError:
            await interaction.response.send_message(embeds=[embed, order_embed], view=DonationAndPromoCodeButtons(self.bot))

    @disnake.ui.button(label="Доп. контакты", style=disnake.ButtonStyle.blurple, custom_id="additional_contacts_button")
    async def additional_contacts_button(self, button: disnake.ui.Button, ctx: disnake.AppCmdInter):
        await ctx.response.send_modal(modal=AdditionalContactsMenu(self.bot))

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(ContinueAndAdtConButtonsReg(bot))

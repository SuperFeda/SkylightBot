import disnake, sqlite3
from disnake.ext import commands

from ssbot import BOT, SSBot
from cogs.hadlers.handlers import color_order
from cogs.view.buttons.donation_and_promo_code_buttons import DonationAndPromoCodeButtons


class ContinueButtonReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ContinueButton was added")
        self.bot.add_view(ContinueButton(bot=self.bot))


class ContinueButton(disnake.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Продолжить", style=disnake.ButtonStyle.green, custom_id="continue_button")
    async def continue_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        channel = BOT.get_channel(1130521980936921200)  # 1130092027942555740 - order channel id

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

        # find service images
        cursor.execute("SELECT service_images FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_images = result[0] if result else None

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

        color = color_order(var_service_type)

        order_embed = disnake.Embed(title='Ваш заказ:', color=color)
        order_embed.add_field(
            name=f'Код заказа: {var_service_code}\nДата оформления: {var_sending_time}\nИмя заказчика: {var_client_display_name} (tag: {var_client_name})\nУслуга: {var_service_type}\nСсылка на экземплы: {var_service_images}',
            value=""
        )
        order_embed.add_field(name="Описание:", value=var_service_description, inline=False)

        if var_mail is not None or var_vk_url is not None or var_telegram_url is not None:
            order_embed.add_field(name="Доп. контакты связи:", value="", inline=False)
            if var_vk_url is not None:
                order_embed.add_field(name=f'ВК: {var_vk_url}', value="", inline=False)
            if var_mail is not None:
                order_embed.add_field(name=f'Эл. почта: {var_mail}', value="", inline=False)
            if var_telegram_url is not None:
                order_embed.add_field(name=f'Телеграм: {var_telegram_url}', value="", inline=False)

        if not interaction.author.avatar or interaction.author.avatar is None:
            order_embed.set_author(name=var_client_display_name)
        else:
            order_embed.set_author(name=var_client_display_name, icon_url=var_client_avatar)

        connection.close()

        await interaction.response.send_message(
            "**В тексте доната *ОБЯЗАТЕЛЬНО* напишите ваш дискорд ник и код заказа, в ином случае заказ не будет выполнен.**\nПроверьте и запомните код заказа.\n\nЕсли заказ не был принят в течении *двух недель*, то свежитесть с нами по этому электронному адресу: skylightservice64@gmail.com. В теме письма укажите код заказа и Discord никнейм, с которого происходил платеж и который **должен** быть указан в донате.",
            embed=order_embed, view=DonationAndPromoCodeButtons(self.bot), ephemeral=True
        )

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(ContinueButtonReg(bot))

import disnake, sqlite3

from disnake.ext import commands

from ssbot import SSBot, BOT
from cogs.hadlers import utils, dicts
from cogs.view.buttons.take_order import TakeOrder
from cogs.view.modals_menu.promo_code_enter import PromoCodeEnterMenu


class DonationAndPromoCodeButtonsReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DonationAndPromoCodeButtons was added")
        self.bot.add_view(DonationAndPromoCodeButtons(bot=self.bot))


class DonationAndPromoCodeButtons(disnake.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Оплатить", style=disnake.ButtonStyle.blurple, custom_id="pay_button")
    async def pay_button(self, button: disnake.ui.Button, ctx):
        button.disabled = True

        user_id = ctx.author.id
        WORKER_ORDER_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["worker_order_channel_id"])

        connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
        cursor = connection.cursor()

        # get client name
        cursor.execute("SELECT client_name FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_name = result[0] if result else None

        # get client id
        cursor.execute("SELECT client_id FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_id = result[0] if result else None

        # get client avatar
        cursor.execute("SELECT client_avatar FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_avatar = result[0] if result else None

        # get client display name
        cursor.execute("SELECT client_display_name FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_client_display_name = result[0] if result else None

        # get service type
        cursor.execute("SELECT service_type FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_type = result[0] if result else None

        # get service description
        cursor.execute("SELECT service_description FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_description = result[0] if result else None

        # get service code
        cursor.execute("SELECT service_code FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_service_code = result[0] if result else None

        # get sending time
        cursor.execute("SELECT sending_time FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_sending_time = result[0] if result else None

        # get vk
        cursor.execute("SELECT vk_url FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_vk_url = result[0] if result else None

        # get mail
        cursor.execute("SELECT mail FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_mail = result[0] if result else None

        # get telegram url
        cursor.execute("SELECT telegram_url FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_telegram_url = result[0] if result else None

        # get active promo code
        cursor.execute("SELECT active_promo_code FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_active_promo_code = result[0] if result else None

        # get youtube promo code counter
        cursor.execute("SELECT youtube_promo_code_counter FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_youtube_promo_code_counter = result[0] if result else None

        connection.close()

        color = utils.color_order(var_service_type)  # получение цвета для embed

        order_embed = disnake.Embed(title='Новый заказ:', color=color)
        order_embed.add_field(name=f'Код заказа: {var_service_code}\nДата оформления: {var_sending_time} (МСК / GMT+3)\nИмя заказчика: {var_client_display_name} (tag: {var_client_name})', value="")
        order_embed.add_field(name='Услуга:', value=var_service_type, inline=False)
        order_embed.add_field(name='ID заказчика:', value=var_client_id, inline=False)
        order_embed.add_field(name="Описание:", value=var_service_description, inline=False)

        if var_active_promo_code is not None:
            order_embed.add_field(name="Активированный промокод:", value=var_active_promo_code, inline=False)

        if var_mail != "" and var_mail is not None or var_vk_url != "" and var_vk_url is not None or var_telegram_url != "" and var_telegram_url is not None:
            order_embed.add_field(name="Доп. контакты связи:", value="", inline=False)
            if var_vk_url != "" and var_vk_url is not None:
                order_embed.add_field(name=f'VK: {var_vk_url}', value="", inline=False)
            if var_mail != "" and var_mail is not None:
                order_embed.add_field(name=f'Электронная почта: {var_mail}', value="", inline=False)
            if var_telegram_url != "" and var_telegram_url is not None:
                order_embed.add_field(name=f'Telegram: {var_telegram_url}', value="", inline=False)

        avatar = utils.get_avatar(ctx_user_avatar=ctx.author.avatar)

        order_embed.set_author(name=var_client_display_name, icon_url=avatar)

        if var_youtube_promo_code_counter is not None:
            if var_youtube_promo_code_counter < 1:
                connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO settings (user_id, promo_code_activated, youtube_promo_code_counter, active_promo_code) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET promo_code_activated=?, active_promo_code=?, youtube_promo_code_counter=?",
                    (user_id, False, None, None, False, None, None)
                )
                connection.commit()
                connection.close()
            else:
                var_youtube_promo_code_counter -= 1
                connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO settings (user_id, youtube_promo_code_counter, promo_code_activated, active_promo_code) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET youtube_promo_code_counter=?, promo_code_activated=?, active_promo_code=?",
                    (user_id, var_youtube_promo_code_counter, True, var_active_promo_code, var_youtube_promo_code_counter, True, var_active_promo_code)
                )
                connection.commit()
                connection.close()

        cash_for_pay = ""
        if var_active_promo_code is not None:
            file = utils.read_json(path=SSBot.PATH_TO_PROMO_CODES_DATA)
            len_active_promo_code = len(var_active_promo_code)
            percentage = 0

            if len_active_promo_code == 10:
                connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO settings (user_id, promo_code_activated, youtube_promo_code_counter, active_promo_code) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET promo_code_activated=?, active_promo_code=?, youtube_promo_code_counter=?",
                    (user_id, False, None, None, False, None, None)
                )
                connection.commit()
                connection.close()

                percentage = file["common_code"][var_active_promo_code]["discount_rate"]

            elif len_active_promo_code == 17:
                percentage = file["youtube_code"][var_active_promo_code]["discount_rate"]

            cash_for_pay = f"\nТ.к. вы использовали промокод {var_active_promo_code} на скидку {percentage}%, то оплата будет в размере {int(utils.calc_percentage(promo_code=var_active_promo_code, price=dicts.SERVICE_PRICES[var_service_type]))}₽."

        if var_service_type in SSBot.NOT_STATIC_PRICE:
            pay_message = "Ваш заказ был отправлен мастерам SkylightServices. Скоро с вами свяжется один из мастеров."  # Добавить уведомление о том, что с заказчиком скоро свяжутся
            cash_for_pay = "\nСсылку для оплаты вам предоставят после связи с сотрудником."
        else:
            pay_message = "Ваш заказ был отправлен сотрудникам SkylightServices. Скоро с вами свяжется один из мастеров.\nСсылка для оплаты: https://www.donationalerts.com/r/skylightservice ."

        embed = disnake.Embed(title="Заказ отправлен", color=disnake.Color.blurple())
        embed.add_field(name="".join([pay_message, cash_for_pay]), value="")

        try:
            pictures = utils.get_files(f"cache/{ctx.author.name}/")

            await WORKER_ORDER_CHANNEL.send(embed=order_embed, view=TakeOrder(self.bot), files=pictures)

            utils.delete_files_from_cache(author_name=ctx.author.name)
        except FileNotFoundError:
            await WORKER_ORDER_CHANNEL.send(embed=order_embed, view=TakeOrder(self.bot))

        await ctx.response.edit_message(view=self)
        await ctx.send(embed=embed)

    @disnake.ui.button(label="Ввести промокод", style=disnake.ButtonStyle.blurple, custom_id="promo_code_button")
    async def promo_code_button(self, button: disnake.ui.Button, ctx: disnake.AppCmdInter):
        await ctx.response.send_modal(modal=PromoCodeEnterMenu(self.bot))

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(DonationAndPromoCodeButtonsReg(bot))

import disnake, sqlite3
from disnake.ext import commands

from ssbot import SSBot
from cogs.hadlers import utils


# Класс для регистрации этого файла как кога, чтобы его можно было загрузить в main
class PromoCodeEnterReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("PromoCodeEnter was added")
        self.bot.add_view(PromoCodeEnterMenu(bot=self.bot))


class PromoCodeEnterMenu(disnake.ui.Modal):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            title="Ввод промокода", custom_id="promo_code_enter",
            timeout=200.0, components=[
                disnake.ui.TextInput(
                    label="Промокод",
                    placeholder="Введите промокод",
                    custom_id="promo_code",
                    style=disnake.TextInputStyle.short,
                    max_length=17,
                )
            ]
        )

    async def callback(self, ctx):
        promo_codes_data = utils.read_json(path=SSBot.PATH_TO_PROMO_CODES_DATA)  # подгрузка файла с данными о промокодами
        value_from_enter_modal_menu = ctx.text_values["promo_code"]  # Получение данных введенных в TextInput под id "promo_code" в модальном меню
        user_id = ctx.author.id

        promo_code_type = "common_code"
        if len(value_from_enter_modal_menu) == 17:
            promo_code_type = "youtube_code"

        if value_from_enter_modal_menu in promo_codes_data[promo_code_type]:
            async with ctx.channel.typing():
                connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
                cursor = connection.cursor()

                # Получение значения, которое говорит, есть ли уже активный промокод у мембера или нет
                cursor.execute("SELECT promo_code_activated FROM settings WHERE user_id=?", (user_id,))
                result = cursor.fetchone()
                promo_code_activated_var = result[0] if result else None

                # Найти список с веденными промокодами
                cursor.execute("SELECT activated_promo_codes_list FROM settings WHERE user_id=?", (user_id,))
                result = cursor.fetchone()
                activated_promo_codes_list_var = result[0] if result else None

                connection.close()

                user_codes = utils.string_to_list(activated_promo_codes_list_var)
                flag = False
                for code in user_codes:
                    if value_from_enter_modal_menu == code:
                        flag = True
                        break

                if flag is True:
                    embed = utils.create_embed(title="Промокод недействителен", color=disnake.Color.red(), content="Данный промокод уже был введён ранее на вашем аккаунте.")
                    return await ctx.send(embed=embed)
                if promo_code_activated_var is True:
                    embed = utils.create_embed(title="Промокод не активирован", color=disnake.Color.red(), content="У вас уже есть активированный промокод.")
                    return await ctx.send(embed=embed)

                youtube_codes_data = None
                user_can_activate_promo_code_flag = False
                if len(value_from_enter_modal_menu) == 17:
                    youtube_codes_data = promo_codes_data["youtube_code"][value_from_enter_modal_menu]["count"]

                    if "users" in promo_codes_data["youtube_code"][value_from_enter_modal_menu]:
                        for pr_user_id in promo_codes_data["youtube_code"][value_from_enter_modal_menu]["users"]:
                            if pr_user_id == ctx.author.id:
                                user_can_activate_promo_code_flag = True
                                break
                        if user_can_activate_promo_code_flag is False:
                            embed = utils.create_embed(title="Промокод недействителен", color=disnake.Color.red(), content="Вы не можете активировать этот промокод потому что вас не в списке пользователей, которым он доступен.")
                            return await ctx.send(embed=embed)

                if "count_for_use" in promo_codes_data[promo_code_type][value_from_enter_modal_menu]:
                    if promo_codes_data[promo_code_type][value_from_enter_modal_menu]["count_for_use"] < 1:
                        embed = utils.create_embed(title="Промокод недействителен", color=disnake.Color.red(), content="Этот промокод больше нельзя использовать.")
                        return await ctx.send(embed=embed)
                    promo_codes_data[promo_code_type][value_from_enter_modal_menu]["count_for_use"] -= 1
                    utils.write_json(SSBot.PATH_TO_CODES, promo_codes_data)

                connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO settings (user_id, youtube_promo_code_counter) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET youtube_promo_code_counter=?",
                    (user_id, youtube_codes_data, youtube_codes_data)
                )
                connection.commit()
                connection.close()

                activated_promo_codes_list_var += value_from_enter_modal_menu+","

                connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO settings (user_id, promo_code_activated, activated_promo_codes_list, active_promo_code) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET promo_code_activated=?, activated_promo_codes_list=?, active_promo_code=?",
                    (user_id, True, activated_promo_codes_list_var, value_from_enter_modal_menu, True, activated_promo_codes_list_var, value_from_enter_modal_menu)
                )
                connection.commit()
                connection.close()

                promo_code_activated = utils.create_embed(title="Промокод активирован", color=SSBot.DEFAULT_COLOR, content=f"Промокод {value_from_enter_modal_menu} успешно активирован.")
            await ctx.send(embed=promo_code_activated)

        else:
            embed = utils.create_embed(title="Промокод недействителен", color=disnake.Color.red(), content="Такого промокода нету в базе данных.")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PromoCodeEnterReg(bot))

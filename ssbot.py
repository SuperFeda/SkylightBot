import disnake, sqlite3, os
from disnake.ext import commands

from cogs.hadlers.handlers import read_json

#####################################
#                                   #
# Самый говнокод из всех говнокодов #
#                                   #
# Python 3.10                       #
# disnake 2.9.1                     #
# colorama 0.4.6                    #
# numpy 1.25.2                      #
#                                   #
#####################################


class SSBot(commands.Bot):  # main класс бота
    # Константы
    BOT_CONFIG = read_json("./data/bot_config.json")
    PATH_TO_CLIENT_DB = "data/skylightbot_client_base.db"
    PATH_TO_WORKER_DB = "data/skylightbot_worker_base.db"
    PATH_TO_PROMO_CODES_DATA = "data\\promo_codes.json"
    PATH_TO_CODES = "data/codes.json"
    DEFAULT_COLOR = disnake.Color.from_rgb(43, 45, 49)
    SKIN64 = "Скин 64x64"
    SKIN128 = "Скин 128x128"
    SKIN_4D = "4D скин"
    MODEL = "Модель"
    ANIM_MODEL = "Модель + анимация"
    TEXTURE_MODEL = "Модель + текстура"
    ANIM_TEXTURE_MODEL = "Модель + анимация + текстура"
    CAPE = "Плащ"
    TOTEM = "Тотем"
    TOTEM_3D = "3D тотем"
    TEXTURE = "Текстура блока/предмета"
    LETTER_LOGO = "Буквенный логотип"
    LETTER_LOGO_2 = "Логотип с кастомными буквами/доп. деталями"
    CHARACTERS_DESIGN = "Дизайн персонажей"
    SPIGOT_PLUGIN = "Spigot плагин"
    NOT_STATIC_PRICE = (MODEL, ANIM_MODEL, TEXTURE_MODEL, ANIM_TEXTURE_MODEL, LETTER_LOGO_2, SPIGOT_PLUGIN)

    def __init__(self):
        super().__init__(
            command_prefix="!",
            help_command=None,
            intents=disnake.Intents.all(),
            test_guilds=[1130086027885809675],
            owner_id=875246294044643371
        )


def load_cogs():  # def для загрузки когов бота
    # load bot commands
    for filename in os.listdir("./cogs/commands"):
        if filename.endswith(".py"):
            BOT.load_extension(f'cogs.commands.{filename[:-3]}')

    # load buttons
    for filename in os.listdir("./cogs/view/buttons"):
        if filename.endswith(".py"):
            BOT.load_extension(f'cogs.view.buttons.{filename[:-3]}')

    # load modals menus
    for filename in os.listdir("./cogs/view/modals_menu"):
        if filename.endswith(".py"):
            BOT.load_extension(f'cogs.view.modals_menu.{filename[:-3]}')

    BOT.load_extension("cogs.events")  # load bot events
    BOT.load_extension("cogs.view.service_select")  # load ServiceSelect menu


connection = sqlite3.connect('./data/skylightbot_worker_base.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        user_id INTEGER PRIMARY KEY,
        worker_salary,
        worker_tag,
        worker_display_name,
        worker_id
    )
""")

connection_ = sqlite3.connect('./data/skylightbot_client_base.db')
cursor_ = connection_.cursor()
cursor_.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        user_id INTEGER PRIMARY KEY,
        client_name,
        client_id,
        client_avatar,
        client_display_name,
        client_guild_permissions, 
        activated_promo_codes_list,
        active_promo_code,
        promo_code_activated,
        youtube_promo_code_counter,
        service_type,
        service_description,
        service_code,
        sending_time,
        order_message,
        order_embed,
        mail,
        vk_url,
        telegram_url
    )
""")

########### Команда для тестов embed настороек
# @bot.slash_command()
# async def show_user(ctx, member: disnake.Member):
#     embed = disnake.Embed(title="Информация о пользователе", description=f"Никнейм: {member.display_name}", color=disnake.Color.blue())
#
#     if not member.avatar:
#         embed.set_author(name=member.display_name)
#     else:
#         embed.set_author(name=member.display_name, icon_url=member.avatar.url)
#
#     await ctx.send(embed=embed)
###########

BOT = SSBot()

# if __name__ == "__main__":
BOT.i18n.load("./lang/")  # Подгрузка файлов локализации
load_cogs()

BOT.run(os.environ["SSBOT_TOKEN"])
#BOT.run("MTEzODc2MTE1ODIxMjQ2ODgxNg.GIF6Po.OAJBKFGlAJ-hMm2uI8pij6xb32JLBLNDivTYjw")

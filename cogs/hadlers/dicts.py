from ssbot import SSBot

# Цены всех услуг
# Этот dict еще используется для подсчета зарплат сотрудников, поэтому у некоторых услуг значение стоимости = 0
SERVICE_PRICES = {
    SSBot.SKIN64: 270,
    # "Скин 128x128": ,
    # "4D Скин": ,

    SSBot.MODEL: 0,
    SSBot.ANIM_MODEL: 0,
    SSBot.TEXTURE_MODEL: 0,
    # "Модель + GeckoLib анимация + текстура": ,

    SSBot.CAPE: 99,
    SSBot.TOTEM: 59,
    # "3D тотем со скином игрока": 0,
    SSBot.TEXTURE: 79,

    SSBot.LETTER_LOGO: 249,
    SSBot.LETTER_LOGO_2: 0,

    SSBot.CHARACTERS_DESIGN: 700,

    # "Spigot плагин": 0
}

# Цены услуг с нестатическим ценником
NOT_STATIC_PRICE = {
    SSBot.MODEL: 149,
    SSBot.ANIM_MODEL: 159,
    SSBot.TEXTURE_MODEL: 159,
    SSBot.LETTER_LOGO_2: 249,
    SSBot.SPIGOT_PLUGIN: "Цена договорная"
}

# Вид того, как должен выглядеть файл promo_codes.json из папки data без данных о промокодах (я не знаю зачем это здесь)
BASE_PC_FILE = {
  "common_code": {},
  "youtube_code": {}
}

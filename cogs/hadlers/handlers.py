import string, random, os, numpy, json, disnake
from colorama import Fore


# def for test of variables
def var_test(variable: vars):
    print(f"{Fore.CYAN}var type: {type(variable)}\noutput: {variable}{Fore.RESET}")


# read json file
def read_json(path: str):
    with open(path, 'r') as json_file:
        return json.load(json_file)


# write json file
def write_json(path: str, data: dict):
    with open(path, 'w') as json_file:
        return json.dump(data, json_file, indent=4, ensure_ascii=False)


# convert "123456789,FFFFFFFFF,AAAAAAAAA," to ['23456789', 'FFFFFFFFF', 'AAAAAAAAA']
def string_to_list(string: str) -> list:
    list_ = []
    result = ""
    for symbol in string:
        if symbol == ",":
            list_.append(result.replace(result[0], ""))
            result = ""
        result += symbol

    return list_


# calculate percentage of discount for price
def calc_percentage(promo_code: str, price: int):
    promo_codes_json = read_json(path="data\\promo_codes.json")
    if len(promo_code) == 10:
        return price - (price * promo_codes_json["common_code"][promo_code]["discount_rate"] / 100)
    elif len(promo_code) == 17:
        return price - (price * promo_codes_json["youtube_code"][promo_code]["discount_rate"] / 100)
    else:
        return print(f"{Fore.RED}[ERR]{Fore.RESET} Error in calc_percentage def")


# generate random combination of order id
def generate_random_combination(length: int):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in numpy.arange(length))


# select color for order
def color_order(var: vars):
    from ssbot import SSBot

    if var in (SSBot.SKIN64, SSBot.SKIN128, SSBot.SKIN_4D):
        return disnake.Color.blue()
    elif var in (SSBot.MODEL, SSBot.ANIM_MODEL, SSBot.ANIM_TEXTURE_MODEL, SSBot.TEXTURE_MODEL):
        return disnake.Color.brand_red()
    elif var in (SSBot.CAPE, SSBot.TOTEM, SSBot.TOTEM_3D, SSBot.TEXTURE):
        return disnake.Color.orange()
    elif var in (SSBot.LETTER_LOGO, SSBot.LETTER_LOGO_2):
        return disnake.Color.blurple()
    elif var in (SSBot.CHARACTERS_DESIGN):
        return disnake.Color.dark_orange()
    elif var in (SSBot.SPIGOT_PLUGIN):
        return disnake.Color.magenta()
    else:
        return disnake.Color.default()


# select color for archive request
def color_archive_request(var: vars):
    if var == "покупка":
        return disnake.Color.blue()
    elif var == "предложение":
        return disnake.Color.green()
    else:
        return disnake.Color.default()


# get files from folder
def get_files(path: str) -> list:
    picture_for_send = []
    for image_for_send in os.listdir(path):
        picture_for_send.append(disnake.File(path+f"{image_for_send}"))

    return picture_for_send


# no use
def delete_files(username):
    for delete_file in os.listdir("cache"):
        if os.path.isfile(os.path.join("cache", delete_file)):
            filename, extension = os.path.splitext(delete_file)
            if username in filename:
                os.remove(os.path.join("cache", delete_file))

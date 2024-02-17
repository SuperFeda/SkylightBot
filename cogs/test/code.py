# codes = "123456789,FFFFFFFFF,AAAAAAAAA,"
# codes_12 = "1234567890,"
#
#
# def string_to_list(string: str) -> list:
#     list_ = []
#     result = ""
#     for symbol in string:
#         if symbol == ",":
#             list_.append(result.replace(result[0], ""))
#             result = ""
#         result += symbol
#
#     return list_
# # for symbol in string:
# #     if symbol == ",":
# #         listok.append(itog)
# #         itog = None
# #     itog = "".join(symbol for symbol in string if symbol != ",", break)
#
#
# codes_list = string_to_list(codes_12)
# print(codes_list)
#
# add_new_code = input("enter new code >> ")
# codes_12 += add_new_code+","
# print(f"{codes_12 = }")
#
# new_code_list = string_to_list(codes_12)
# print(f"{new_code_list = }")

def calc_percentage(promo_code: str|None, price: int):
    return price - (price * 20 / 100)
print(calc_percentage(price=0, promo_code=None))


# text = "text"
# new_text = ''
# print("".join([text, new_text]))


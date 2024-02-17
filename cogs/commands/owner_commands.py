import disnake, sqlite3
from disnake.ext import commands
from disnake import Localized

from ssbot import BOT, SSBot
from cogs.hadlers import handlers, bot_choices
from cogs.view.service_select import ServiceSelectView


class OwnerCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="panel_summon")
    async def panel_summon(self, ctx):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        embed = disnake.Embed(title="SkylightServices", color=disnake.Color.blurple())
        embed.add_field(
            name="Посмотреть список услуг: <#1130088587661148290>\nОтзывы: <#1130088521718300682>\n\n**Перед оформлением заказа не забудьте прочитать пользовательское соглашение в канале** <#1169299255597469696>",
            value=""
        )

        superfeda = BOT.get_user(875246294044643371)

        file = disnake.File("SkylightServices_new.png", filename="image.jpg")
        embed.set_image(url="attachment://image.jpg")
        embed.set_footer(
            text=f"{superfeda.display_name}: Вы автоматически соглашаетесь с пользовательским соглашением после оформления заказа",
            icon_url=superfeda.avatar
        )

        ORDER_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["order_channel_id"])

        await ORDER_CHANNEL.send(embed=embed, file=file, view=ServiceSelectView(self.client))

    @commands.slash_command(name="get_salary_list")
    async def get_salary_list(self, ctx):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды", ephemeral=True)

        connection = sqlite3.connect('data/skylightbot_worker_base.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings")
        result = cursor.fetchall()
        connection.close()

        workers_salary_embed = disnake.Embed(title="Список зарплат:", colour=disnake.Color.blurple())
        for num, item in enumerate(result):
            workers_salary_embed.add_field(name=f"{num+1}) {item[3]} ({item[2]}): {item[1]}₽", value="", inline=False)

        await ctx.send(embed=workers_salary_embed, ephemeral=True)

    @commands.slash_command(name="reset_all_workers_salary")
    async def reset_all_workers_salary(self, ctx):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        connection = sqlite3.connect('data/skylightbot_worker_base.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings")
        result = cursor.fetchall()
        connection.close()

        for item in result:
            connection = sqlite3.connect('./data/skylightbot_worker_base.db')
            cursor = connection.cursor()
            user_id = item[0]
            cursor.execute(
                "INSERT INTO settings (user_id, worker_salary) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET worker_salary=?",
                (user_id, 0, 0)
            )
            connection.commit()
            connection.close()

        await ctx.send("Зарплаты аннулированы.", ephemeral=True)

    @commands.slash_command(name="edit_one_worker_salary")
    async def edit_one_worker_salary(self, ctx, worker: disnake.Member, salary: int):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        connection = sqlite3.connect('data/skylightbot_worker_base.db')
        cursor = connection.cursor()
        user_id = worker.id
        cursor.execute("SELECT worker_salary FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_worker_salary = result[0] if result else None
        connection.close()

        connection = sqlite3.connect('./data/skylightbot_worker_base.db')
        cursor = connection.cursor()
        user_id = worker.id
        cursor.execute(
            "INSERT INTO settings (user_id, worker_salary) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET worker_salary=?",
            (user_id, salary, salary)
        )
        connection.commit()
        connection.close()

        await ctx.send(f"Зарплата для {worker.display_name} изменена с {var_worker_salary}₽ на {salary}₽", ephemeral=True)

    @commands.slash_command(name="edit_all_worker_salary")
    async def edit_all_worker_salary(self, ctx, salary: int, sure: bool = commands.Param(
        choices=bot_choices.CHOICE_FOR_SURE, description=Localized("Are you sure?", key="edit_all_worker_salary.sure.description")
                )):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        if sure is False or sure is None:
            return await ctx.send(f"{sure = }", ephemeral=True)

        connection = sqlite3.connect('./data/skylightbot_worker_base.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings")
        result = cursor.fetchall()
        connection.close()

        embed = disnake.Embed(title="Изменения зарплат:", color=disnake.Color.blurple())

        for item in result:
            embed.add_field(name=f"Зарплата {item[3]} ({item[2]}) изменена с {item[1]}₽ на {salary}₽", value='', inline=False)

            connection = sqlite3.connect('./data/skylightbot_worker_base.db')
            cursor = connection.cursor()
            user_id = item[0]
            cursor.execute(
                "INSERT INTO settings (user_id, worker_salary) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET worker_salary=?",
                (user_id, salary, salary)
            )
            connection.commit()
            connection.close()

        await ctx.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="for_delete")
    async def for_delete(self, ctx):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        await ctx.channel.purge()

    @commands.slash_command(name="add_promo_code")
    async def add_promo_code(self, ctx, promo_code_name: str, discount_rate: int, count: int | None = None, pc_type: str = commands.Param(choices=bot_choices.CHOICE_FOR_PC_TYPE)):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        pc_data = handlers.read_json(path="data\\promo_codes.json")

        if pc_type == "common_code":
            if len(promo_code_name) != 10:
                return await ctx.send("Промокод для категории \"common_code\" должен иметь длинну в 10 символов!", ephemeral=True)
            if discount_rate > 99:
                return await ctx.send("`discount_rate` должен быть не больше 99%!", ephemeral=True)
            if count is not None:
                return await ctx.send("Промокоды категории \"common_code\" не поддерживают count!", ephemeral=True)
            if promo_code_name in pc_data["common_code"]:
                return await ctx.send(f"Промокод **{promo_code_name}** уже есть в базе данных.", ephemeral=True)

            pc_data["common_code"].update({promo_code_name: {"discount_rate": discount_rate}})

        elif pc_type == "youtube_code":
            if len(promo_code_name) != 17:
                return await ctx.send("Промокод для категории \"youtube_code\" должен иметь длинну в 17 символов!", ephemeral=True)
            if count is None:
                return await ctx.send("Для промокода типа \"youtube_code\" параметр \"count\" - обязателен!", ephemeral=True)
            if count < 2:
                return await ctx.send("count должен иметь значение не меньше 2!", ephemeral=True)
            if discount_rate > 99:
                return await ctx.send("discount_rate должен быть не больше 99%!", ephemeral=True)
            if promo_code_name in pc_data["youtube_code"]:
                return await ctx.send(f"Промокод **{promo_code_name}** уже есть в базе данных.", ephemeral=True)

            pc_data["youtube_code"].update({promo_code_name: {"discount_rate": discount_rate, "count": count-1}})

        handlers.write_json(path="data\\promo_codes.json", data=pc_data)

        await ctx.send(f"Промокод **{promo_code_name}** добавлен в базу данных в категорию \"{pc_type}\".", ephemeral=True)

    @commands.slash_command(name="remove_promo_code")
    async def remove_promo_code(self, ctx, promo_code_name: str, pc_type: str = commands.Param(choices=bot_choices.CHOICE_FOR_PC_TYPE)):
        if ctx.author.name != "superfeda" and ctx.author.id != 875246294044643371:
            return await ctx.send("У вас нет прав на использование этой команды.", ephemeral=True)

        pc_data = handlers.read_json(path="data\\promo_codes.json")
        pc_data[pc_type].pop(promo_code_name)
        handlers.write_json(path="data\\promo_codes.json", data=pc_data)

        await ctx.send(f"Промокод {promo_code_name} удален из базы данных.", ephemeral=True)

    # @commands.slash_command(name="menu")  # command for check promo code modal menu
    # async def menu(self, ctx: disnake.AppCmdInter):
    #     await ctx.response.send_modal(modal=PromoCodeEnter(self.client))


def setup(client):
    client.add_cog(OwnerCommands(client))

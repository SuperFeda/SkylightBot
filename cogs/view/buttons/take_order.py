import disnake, sqlite3
from disnake.ext import commands

from ssbot import SSBot
from cogs.hadlers import dicts, utils


def for_in_embed(in_: dict) -> str:
    data = None
    for key_, value_ in in_:
        if key_ == "value":
            data = value_
            break

    return data


class TakeOrderReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("TakeOrder was added")
        self.bot.add_view(TakeOrder(bot=self.bot))


class TakeOrder(disnake.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, custom_id="take_order_button")
    async def take_order_button(self, button: disnake.ui.Button, ctx):
        worker_id = ctx.author.id
        category = disnake.utils.get(ctx.guild.categories, id=SSBot.BOT_CONFIG["orders_category_id"])
        client_order_message = await ctx.channel.fetch_message(ctx.message.id)
        service_type_from_embed = for_in_embed(in_=client_order_message.embeds[0]._fields[1].items())  # getting client service type from embed
        client_id_from_embed = int(for_in_embed(in_=client_order_message.embeds[0]._fields[2].items())) # getting client id from his order embed
        avatar = utils.get_avatar(ctx_user_avatar=ctx.author.avatar)

        enter_promo_code_from_embed = None
        flag, flag_2 = False, False
        try:
            for key_, value_ in client_order_message.embeds[0]._fields[4].items():  # getting enter promo code
                if key_ == "name" and value_ == "Активированный промокод:":
                    flag_2 = True
                if key_ == "value" and flag_2 is True:
                    enter_promo_code_from_embed = value_
                    flag = True
                    break
        except IndexError:
            pass

        connection = sqlite3.connect(SSBot.PATH_TO_CLIENT_DB)
        cursor = connection.cursor()

        # find client name
        cursor.execute("SELECT client_name FROM settings WHERE user_id=?", (client_id_from_embed,))
        result = cursor.fetchone()
        var_client_name = result[0] if result else None

        connection.close()

        try:  # if worker is in database:
            connection_ = sqlite3.connect(SSBot.PATH_TO_WORKER_DB)
            cursor_ = connection_.cursor()
            cursor_.execute("SELECT worker_salary FROM settings WHERE user_id=?", (worker_id,))
            result_ = cursor_.fetchone()
            var_worker_salary = result_[0] if result else None

            if flag:
                var_worker_salary = int(var_worker_salary) + utils.calc_percentage(promo_code=enter_promo_code_from_embed, price=dicts.SERVICE_PRICES[service_type_from_embed])
            else:
                var_worker_salary = int(var_worker_salary) + dicts.SERVICE_PRICES[service_type_from_embed]

            connection_.close()
            utils.var_test(var_worker_salary)
            connection_ = sqlite3.connect(SSBot.PATH_TO_WORKER_DB)
            cursor_ = connection_.cursor()
            cursor_.execute(
                "INSERT INTO settings (user_id, worker_salary) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET worker_salary=?",
                (worker_id, var_worker_salary, var_worker_salary)
            )
            connection_.commit()
            connection_.close()

        except TypeError:  # else:
            if flag:
                var_worker_salary_2 = utils.calc_percentage(promo_code=enter_promo_code_from_embed, price=dicts.SERVICE_PRICES[service_type_from_embed])
            else:
                var_worker_salary_2 = dicts.SERVICE_PRICES[service_type_from_embed]
            utils.var_test(var_worker_salary_2)
            connection_ = sqlite3.connect(SSBot.PATH_TO_WORKER_DB)
            cursor_ = connection_.cursor()
            cursor_.execute(
                "INSERT INTO settings (user_id, worker_salary, worker_tag, worker_display_name, worker_id) VALUES (?, ?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET worker_salary=?, worker_tag=?, worker_display_name=?, worker_id=?",
                (worker_id, int(var_worker_salary_2), ctx.author.name, ctx.author.display_name, ctx.author.id, int(var_worker_salary_2), ctx.author.name, ctx.author.display_name, ctx.author.id)
            )
            connection_.commit()
            connection_.close()

        if ctx.author.id == client_id_from_embed:
            permissions = {
                ctx.guild.default_role: disnake.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
                ctx.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
            }
        else:
            permissions = {
                ctx.guild.default_role: disnake.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
                ctx.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True),
                ctx.guild.get_member(client_id_from_embed): disnake.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
            }

        channel = await ctx.guild.create_text_channel(
            name=f"{var_client_name}-{service_type_from_embed}",
            category=category, overwrites=permissions
        )

        embed = client_order_message.embeds[0]
        embed.set_footer(text=f"Заказ принял: {ctx.author.display_name}", icon_url=avatar)

        if service_type_from_embed == SSBot.SKIN64:
            skin_questions = disnake.Embed(
                title="Дополнительные вопросы",
                color=SSBot.DEFAULT_COLOR,
                description="Для того чтобы мы выполнили ваш заказа так, как хотите вы, нам нужно знать ещё кое-какую информацию. Пожалуйста, ответьте на вопросы ниже:"
            ).add_field(name="1) Ваш скин должен иметь стандартные руки или тонкие?", value="", inline=False)

            await channel.send(f"<@{client_id_from_embed}> ,", embed=skin_questions)

        elif service_type_from_embed == SSBot.LETTER_LOGO or service_type_from_embed == SSBot.LETTER_LOGO_2:
            file = disnake.File("images/logos.png", filename="logos.jpg")

            logo_questions = disnake.Embed(
                title="Дополнительные вопросы",
                color=SSBot.DEFAULT_COLOR,
                description="Для того чтобы мы выполнили ваш заказа так, как хотите вы, нам нужно знать ещё кое-какую информацию. Пожалуйста, ответьте на вопросы ниже:"
            ).add_field(name="1) В логотипе должны быть пробелы между словами?", value="", inline=False).set_image(url=f"attachment://logos.jpg")

            await channel.send(f"<@{client_id_from_embed}> ,", embed=logo_questions, file=file)

        # elif service_type_from_embed == SSBot.TEXTURE:
        #     texture_questions = disnake.Embed(
        #         title="Дополнительные вопросы",
        #         color=SSBot.DEFAULT_COLOR,
        #         description="Для того чтобы мы выполнили ваш заказа так, как хотите вы, нам нужно знать ещё кое-какую информацию. Пожалуйста, ответьте на вопросы ниже:"
        #     ).add_field(name="1) Какое должно быть качество у текстуры: 16х16 или 32х32?", value="", inline=False)
        #
        #     await channel.send(f"<@{client_id_from_embed}> ,", embed=texture_questions)

        elif service_type_from_embed == SSBot.CHARACTERS_DESIGN:
            character_questions = disnake.Embed(
                title="Дополнительные вопросы",
                color=SSBot.DEFAULT_COLOR,
                description="Для того чтобы мы выполнили ваш заказа так, как хотите вы, нам нужно знать ещё кое-какую информацию. Пожалуйста, ответьте на вопросы ниже:"
            ).add_field(name="1) На персонаже должны быть тени?", value="", inline=False).add_field(name="2) У персонажа должен быть контур?", value="", inline=False)

            await channel.send(f"<@{client_id_from_embed}> ,", embed=character_questions)

        else:
            await channel.send(f"<@{client_id_from_embed}>")

        await channel.send(f"<@{ctx.author.id}>")
        await client_order_message.edit(embed=embed, view=None)

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(TakeOrderReg(bot))

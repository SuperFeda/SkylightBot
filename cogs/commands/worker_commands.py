import disnake, sqlite3

from disnake.ext import commands

from ssbot import BOT, SSBot
from cogs.hadlers import utils


class WorkerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="rp_guide")
    async def rp_guide(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["worker_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(), content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        await ctx.send("""
        `ss_default_totem_pack` - Пример РП для замены текстуры тотема по умолчанию. Просто закиньте новую текстуру в `assets/minecraft/textures/item/` и назовите файл `totem_of_undying`. Предварительно удалив старую текстуру.

`ss_totem_pack` - Пример РП для замены текстуры тотема по переименованию в наковальне. Идите в `assets/minecraft/optifine/cit/tygg/`, там два файла будет. Замените `superfeda.png` на новую текстуру, для удобства назовите ее также как и клиента, не используя буквы верхнего регистра (капс), цифры и спец символы (%:*?;#&). Второй файл "`superfeda.properties`", назовите ее также, как текстуру, после чего откройте. Перед вами должен быть такой текст:
```properties
type=item
matchItems=totem_of_undying
texture=superfeda.png
nbt.display.Name=SuperFeda
````texture` - Текстура, отображаемая после переименования, замените ее на название текстуры, с учетом формата файла (нужно использовать только `.png`). 
`nbt.display.Name` - Название, которое нужно ввести в наковальне для смены текстуры. Вводите туда имя, которое нужно клиенту.
        """, files=[disnake.File("data/ss_default_totem_pack.zip"), disnake.File("data/ss_totem_pack.zip")], ephemeral=True)

    @commands.slash_command(name="add_salary")
    async def add_salary(self, ctx, salary: int, promo_code: str | None = None):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["worker_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(), content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        user_id = ctx.author.id
        LOG_CHANNEL = BOT.get_channel(SSBot.BOT_CONFIG["log_channel_id"])

        connection = sqlite3.connect(SSBot.PATH_TO_WORKER_DB)
        cursor = connection.cursor()
        cursor.execute("SELECT worker_salary FROM settings WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        var_worker_salary = result[0] if result else None
        connection.close()

        try:
            if promo_code is not None:
                var_worker_salary_new = int(var_worker_salary) + int(utils.calc_percentage(promo_code, salary))
            else:
                var_worker_salary_new = int(var_worker_salary) + salary
        except TypeError:
            embed = utils.create_embed(title="Ошибка", color=disnake.Color.red(), content="Похоже, что вас ещё нет с базе сотрудников SS. Для того чтобы попасть туда примите хотя бы один заказ.")
            return await ctx.send(embed=embed, ephemeral=True)

        connection_ = sqlite3.connect(SSBot.PATH_TO_WORKER_DB)
        cursor_ = connection_.cursor()
        cursor_.execute(
            "INSERT INTO settings (user_id, worker_salary) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET worker_salary=?",
            (user_id, var_worker_salary_new, var_worker_salary_new)
        )
        connection_.commit()
        connection_.close()

        embed = utils.create_embed(title="Зарплата добавлена", color=disnake.Color.blurple(), content=f"Кол-во добавленной зарплаты: {salary}₽.\nТекущая зарплата: {var_worker_salary_new}₽.")
        log_embed = disnake.Embed(title="Добавление зарплаты", description=f"{ctx.author.display_name} ({ctx.author.name}) **добавил себе {salary}₽** в зарплату.\n\nТекущая зарплата: {var_worker_salary_new}₽;\nЗарплата до: {var_worker_salary}₽;\nКанал в котором была введена команда: <#{ctx.channel.id}>;")

        await ctx.send(embed=embed, ephemeral=True)
        await LOG_CHANNEL.send(embed=log_embed)

    @commands.slash_command(name="check_my_salary")
    async def check_my_salary(self, ctx):
        if disnake.utils.get(ctx.guild.roles, id=SSBot.BOT_CONFIG["worker_role_id"]) not in ctx.author.roles:
            embed = utils.create_embed(title="Не достаточно прав", color=disnake.Color.red(), content="У вас нет прав на использование этой команды.")
            return await ctx.send(embed=embed, ephemeral=True)

        connection = sqlite3.connect(SSBot.PATH_TO_WORKER_DB)
        cursor = connection.cursor()
        cursor.execute("SELECT worker_salary FROM settings WHERE user_id=?", (ctx.author.id,))
        result = cursor.fetchone()
        var_worker_salary = result[0] if result else None
        connection.close()

        embed = utils.create_embed(title="Данные о зарплате", color=disnake.Color.blurple(), content=f"Ваша зарплата: {var_worker_salary}₽")

        await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(WorkerCommands(bot))

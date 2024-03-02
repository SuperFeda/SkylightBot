import disnake

from disnake.ext import commands

from cogs.view.buttons.contact_here_button import ContactHereButton
from ssbot import SSBot


class QuestionSelectReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("QuestionSelect was added")
        self.bot.add_view(QuestionSelectView(bot=self.bot))


class QuestionSelect(disnake.ui.StringSelect):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            placeholder="Какой у вас вопрос?", min_values=1, max_values=1,
            custom_id="question_select", options=[
                disnake.SelectOption(label="Обратная связь", value="connection"),
                disnake.SelectOption(label="Как оформить заказ?", value="how_order"),
                # disnake.SelectOption(label="Как устроена оплата?", value="how_pay"),
                disnake.SelectOption(label="Правки", value="edits"),
                disnake.SelectOption(label="Доп. контакты связи", value="add_contacts"),
                disnake.SelectOption(label="Бот выдает ошибку взаимодействия", value="bot_error"),
                # disnake.SelectOption(label="Как пользоваться архивом?", value="archive"),
                disnake.SelectOption(label="Как стать сотрудником SkylightServices?", value="ss_worker")
            ]
        )

    async def callback(self, ctx):
        embed, select, flag = None, self.values[0], True

        if select == "how_order":
            embed = disnake.Embed(
                title="Как оформить заказ?",
                color=SSBot.DEFAULT_COLOR,
                description=f'Оформить заказ можно перейдя в канал <#{SSBot.BOT_CONFIG["order_channel_id"]}> и нажав на кнопку \"Оформить заказ\".'
            )

        # elif select == "how_pay":
        #     embed = disnake.Embed(
        #         title="Как устроена оплата?",
        #         color=SSBot.DEFAULT_COLOR,
        #         description='Оплата в SkylightServices работает через сервис DonationAlerts. Во время оформления заказа некоторых услуг, я могу сразу отправить ссылку для оплаты, но иногда я этого не делаю. Не делаю я этого потому, что видимо вы заказали '
        #     )

        elif select == "edits":
            embed = disnake.Embed(
                title="Правки",
                color=SSBot.DEFAULT_COLOR,
                description='Для услуг из категории \"Текстура\" и \"Скин\" правки бесплатные, а для остальных услуг каждая правка стоит 150₽.'
            )

        elif select == "bot_error":
            flag = False

            file = disnake.File("images/bot_error.png", filename="bot_error.png")
            embed = disnake.Embed(
                title="Бот выдает ошибку взаимодействия",
                color=SSBot.DEFAULT_COLOR,
                description='Данная ошибка появляется из-за того, что бот не успел обработать запрос за 3 секунды либо по каким-то другим техническим причинам.\nОдной из причин, из-за чего бот не успевает обработать запрос является слабый интернет. Попробуйте временно сократить потребление интернета в доме (например поставить на паузу загрузку игры в Steam) и снова попробовать повзаимодействовать с ботом. А если слабый интерет не временное явление, то попробуйте связаться с нашим менеджером, тогда мы поможем вручную собрать заказ.'
            ).set_image(url="attachment://bot_error.png")

            await ctx.send(embed=embed, file=file, ephemeral=True)

        elif select == "add_contacts":
            flag = False

            file = disnake.File("images/add_contacts_menu.png", filename="add_contacts_menu.jpg")
            embed = disnake.Embed(
                title="Дополнительные контакты для связи",
                color=SSBot.DEFAULT_COLOR,
                description='Во время оформления заказа я попрошу вас заполнить форму, где вам нужно ввести дополнительные контакты для связи с вами. В этой форме не обязательно заполнять каждую графу, если вы хотите предоставить, скажем, электронную почту, то можете написать только её и продолжить оформление заказа.'
            ).set_image(url="attachment://add_contacts_menu.jpg")

            await ctx.send(embed=embed, file=file, ephemeral=True)

        elif select == "archive":
            embed = disnake.Embed(
                title="Как пользоваться архивом?",
                color=SSBot.DEFAULT_COLOR,
                description='Архивом пользоваться легче простого! Специально для работы с архивом была создана команда \"`/архив` (`/archive`)\".\nЕсли вы хотите приобрести уже готовый продукт, то тогда в графе \"имя_продукта\" нужно написать имя желаемого продукта, а в графе \"тип_запроса\" выбрать параметр \"Запрос на покупку\".\nВ случае, если вы хотите предложить свой товар для продажи, снова введите ту-же команду и в \"имя_продукта\" напишите имя товара, который вы предлогаете, а в \"тип_запроса\" выберите \"Предложение\".\n\nИммейте ввиду, если вы не являетесь сотрудником SS, то при продаже материала в архиве, налог будет не 25%, а 35%.'
            )

        elif select == "connection":
            flag = False

            embed = disnake.Embed(
                title="Обратная связь",
                color=SSBot.DEFAULT_COLOR,
                description='Для связи с нами вы можете использовать электронную почту: **skylightservice64@gmail.com**.\nЛибо вы можете нажать на кнопку \"Связаться здесь\" под этим сообщением и через время менеджер свяжется с вами.'
            )

            await ctx.send(embed=embed, view=ContactHereButton(self.bot), ephemeral=True)

        elif select == "ss_worker":
            embed = disnake.Embed(
                title="Как стать сотрудником SkylightServices?",
                color=SSBot.DEFAULT_COLOR,
                description='Для того, чтобы стать сотрудником SkylightServices нужно всего лишь заполнить форму по ссылке: https://forms.gle/oSrLv81sAfCefP4f8'
            )

        if flag:
            await ctx.send(embed=embed, ephemeral=True)


class QuestionSelectView(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(QuestionSelect(self.bot))


def setup(bot):
    bot.add_cog(QuestionSelectReg(bot))

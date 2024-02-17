import disnake
from disnake.ext import commands

from cogs.view.modals_menu.promo_code_enter import PromoCodeEnterMenu


class PromoCodeButtonReg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("PromoCodeButton was added")
        self.bot.add_view(PromoCodeButton(bot=self.bot))


class PromoCodeButton(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Промокод", style=disnake.ButtonStyle.blurple, custom_id="promo_code_button")
    async def promo_code_button(self, button: disnake.ui.Button, ctx: disnake.AppCmdInter):
        await ctx.response.send_modal(modal=PromoCodeEnterMenu(self.bot))

    def to_components(self):
        return super().to_components()


def setup(bot):
    bot.add_cog(PromoCodeButtonReg(bot))

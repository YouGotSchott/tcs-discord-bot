import discord
from discord.ext import commands
from textwrap import wrap

dancing_alpha = {
    "a": "<a:A_:485946596387848197>",
    "b": "<a:B_:485946634165813269>",
    "c": "<a:C_:451229675008819221>",
    "d": "<a:D_:451229727567380480>",
    "e": "<a:E_:451229814129426442>",
    "f": "<a:F_:451229903040413698>",
    "g": "<a:G_:451229971806027776>",
    "h": "<a:H_:451230040219451393>",
    "i": "<a:I_:451230102441951242>",
    "j": "<a:J_:451230161359339520>",
    "k": "<a:K_:451230254199996417>",
    "l": "<a:L_:451230309648695297>",
    "m": "<a:M_:451230370235678728>",
    "n": "<a:N_:451230430814011397>",
    "o": "<a:O_:451230485746810891>",
    "p": "<a:P_:451230540012453888>",
    "q": "<a:Q_:451230603438850058>",
    "r": "<a:R_:451230679112482820>",
    "s": "<a:S_:451230738449301506>",
    "t": "<a:T_:451230797010173962>",
    "u": "<a:U_:451230852588765184>",
    "v": "<a:V_:451230908801089546>",
    "w": "<a:W_:451230963544883241>",
    "x": "<a:X_:451231020667240449>",
    "y": "<a:Y_:451231084185649163>",
    "z": "<a:Z_:451231152397877251>"
}


class DanceIt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def danceit(self, ctx, *args):

        await ctx.message.delete()
        await self.dance_it(ctx, *args)

    async def dance_it(self, ctx, *args):
        output = ''
        for word in args:
            letters = ''
            for letter in word:
                if letter.isalpha():
                    letter = letter.lower()
                    letters += dancing_alpha[letter]
                else:
                    letters += letter
            word = letters
            output += word
            output += '    '
        msgs = wrap(output, 2000)
        for msg in msgs:
            await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(DanceIt(bot))

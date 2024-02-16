import discord
from discord.ext import commands
from prettytable import PrettyTable
import random

class DIRA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    global variables, operators, negations, max_length
    # Beispielaufruf
    variables = ['A', 'B', 'C', 'D','E']
    operators = ['∧','∨','→','↔']
    negations = ['','¬']
    max_length = 5

    @commands.command(brief="Bool Formula Generator. Add + for '∧','∨' and ++ for '∧','∨','→','↔','⊕','⊼','⊽'")
    async def boolgen(self, ctx, extends=None):
        if extends is None:
            operators = ['∧','∨']
        elif extends == "+":
            operators = ['∧','∨','→','↔']
        elif extends == "++":
            operators = ['∧','∨','→','↔','⊕','⊼','⊽']

        def generate_random_boolean_formula():
            if max_length < 1:
                raise ValueError("Maximale Länge muss mindestens 1 sein.")
            if not variables:
                raise ValueError("Es müssen mindestens einige Variablen vorhanden sein.")
            def generate_subformula(length):
                if length == 1:
                    return random.choice(negations)+random.choice(variables)
                else:
                    operator = random.choice(operators)
                    if operator == '¬':
                        subformula = generate_subformula(length - 1)
                    else:
                        left_length = random.randint(1, length - 1)
                        right_length = length - left_length
                        left_subformula = generate_subformula(left_length)
                        right_subformula = generate_subformula(right_length)
                        subformula = f"({left_subformula} {operator} {right_subformula})"
                    return subformula

            return generate_subformula(max_length)
        
        await ctx.send(generate_random_boolean_formula())

    def radixgen0(self, base=None, length=None):
        biggerbase = ["A","B","C","D","E","F"]
        if base is None:
            base = random.randint(2,16)
        if length is None:
            length = random.randint(1,8)
        
        a = [x for x in range(0,length)]
        if base > 10:
            finallist = [x if x < 10 else biggerbase[(x%10)] for x in a ]
        else: finallist = a

        return finallist

    @commands.command()
    async def radixgen(self, ctx, base=None, length=None):
        finallist = self.radixgen0(base, length)
        await ctx.send(f"<{finallist}>{base}")

    @commands.command()
    async def subradixgen(self, ctx, base=None, length=None):
        radix0 = self.radixgen0(base, length)
        radix1 = self.radixgen0(base, length)
        await ctx.send(f"{radix0} - {radix1}")

    @commands.command()
    async def addradixgen(self, ctx, base=None, length=None):
        radix0 = self.radixgen0(base, length)
        radix1 = self.radixgen0(base, length)
        await ctx.send(f"{radix0} + {radix1}")


async def setup(bot):
    await bot.add_cog(DIRA(bot))
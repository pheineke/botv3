import discord
from discord.ext import commands

import random

class DIRA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    global variables, operators, negations, max_length
    # Beispielaufruf
    variables = ['A', 'B', 'C', 'D','E']
    operators = ['∧', '∨']
    negations = ['','¬']
    max_length = 5

    async def boolgen(self, ctx):
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



async def setup(bot):
    await bot.add_cog(DIRA(bot))
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

from prettytable import PrettyTable
import random
import os
import graphviz

class DIRA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    global variables, operators, negations, max_length
    # Beispielaufruf
    

    @app_commands.command(name="boolgen", brief="[DIRA] Bool Formula Generator. Add + for '∧','∨' and ++ for '∧','∨','→','↔','⊕','⊼','⊽'")
    async def boolgen(self, interaction:discord.Interaction, extends=None):
        variables = ['A', 'B', 'C', 'D','E']
        operators = ['∧','∨','→','↔']
        negations = ['','¬']
        max_length = 5
        
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
        
        await interaction.response.send_message(generate_random_boolean_formula())

    def radixgen0(self, base=None, length=None):
        biggerbase = ["A","B","C","D","E","F"]
        if base is None:
            base = random.randint(2,16)
        if length is None:
            length = random.randint(1,8)
        
        a = [random.randint(0,base-1) for x in range(0,length)]
        if base > 10:
            finallist = [x if x < 10 else biggerbase[(x%10)] for x in a ]
        else: finallist = a

        return finallist, base

    @app_commands.command(name="automatagen", brief="[DIRA] Generiert deterministische Automaten")
    async def automatagen(self,interaction:discord.Interaction):
        filename = "custom_bdd.png"

        bdd = graphviz.Digraph(format='png')

        bddvars = ['A','B','C','D','E','F','G']
        varchoice = random.randint(2,len(bddvars)-1)

        lessonvars = bddvars[0:varchoice]

        startnode = random.choice(lessonvars)
        for node in lessonvars:
            if node != startnode:
                bdd.node(node)
            else:
                bdd.node(node, penwidth='2')
                

        edges = []
        
        for x in range(2,len(lessonvars)**2):
            node0 = random.choice(lessonvars)
            node1 = random.choice(lessonvars)
            direction = ["a","b","a,b"]
            edge0 = random.choice(direction)
            if (node0,node1,direction[0]) not in edges and (node0,node1,direction[1]) not in edges and (node0,node1,direction[2]) not in edges:
                edges.append((node0,node1,edge0))
                bdd.edge(node0,node1, label=edge0)
        
        # Speichere das BDD als PNG-Datei
        bdd.render(filename, view=False)

        await interaction.response.send_message(file=discord.File(f"{filename}.png"))
        os.remove(f"./{filename}")
        os.remove(f"./{filename}.png")

        

    @app_commands.command(brief="[DIRA] generiert Radixzahl")
    async def radixgen(self, interaction:discord.Interaction, base=None, length=None):
        finallist, base = self.radixgen0(base, length)
        await interaction.response.send(f"<{finallist}>{base}")

    @app_commands.command(brief="[DIRA] generiert Radixaufgabe", aliases=["rdxcg"])
    async def radixcalcgen(self, interaction:discord.Interaction, base=None, length=None):
        radix0, base = self.radixgen0(base, length)
        radix1, base = self.radixgen0(base, length)
        zeichen = random.choice(["+","-","*","÷",""])
        await interaction.response.send(f"<{radix0}>{base} {zeichen} <{radix1}>{base}".replace("'",""))

    @commands.command(brief="[DIRA] generiert Radix-Additionsaufgabe")
    async def addradixgen(self, interaction:discord.Interaction, base=None, length=None):
        radix0, base = self.radixgen0(base, length)
        radix1, base = self.radixgen0(base, length)
        await interaction.response.send(f"<{radix0}>{base} + <{radix1}>{base}".replace("'",""))


async def setup(bot):
    await bot.add_cog(DIRA(bot))
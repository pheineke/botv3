import subprocess
import httpx
import ollama
from ollama import AsyncClient
import os
import pickle
import json
import asyncio
import random
from datetime import datetime
from pathlib import Path
from collections import deque
###########
import discord
from discord.ext import commands


class MedievalGame:
    def __init__(self, model) -> None:
        self.model = model
        self.botpath = os.getcwd()
        self.allModelPath = self.botpath + "/modules/main/rpgai/modelFiles/"
        self.gameStateDir = self.botpath + "/modules/main/rpgai/gameStates/"

        self.gameStateName = ""
        self.gameStatePath = self.gameStateDir + self.gameStateName

        self.gameStateContent = [{'role': 'system', 'content': 'Messages are given to you like this: "username : message-conent". You respond to the Adventurers Inputs after his or her Name. In this example, the Adventurer (Which is the Player) named something in username says to you "Hi"'}]

    def getInfo(self):
        print(self.model)
        print(self.allModelPath)
        print(self.gameStateDir)
        print(self.gameStateName)
        print(self.gameStatePath)
        print(self.gameStateContent)

    #################

    def loadGame(self, gameStateName=None):
        time = datetime.now().strftime("%H-%M_%d-%m-%Y")
        if gameStateName is None:
            gameStateName = f"gameState-{time}-num{random.randint(0,999)}.txt"

        self.gameStatePath = os.path.join(self.gameStateDir, gameStateName)

        try:
            with open(self.gameStatePath, 'r') as file0:
                self.gameStateContent = json.load(file0)
        except FileNotFoundError:
            # Wenn die Datei nicht gefunden wird, eine leere Liste als gameStateContent setzen
            self.gameStateContent = []
        except Exception as e:
            # Falls es irgendeinen anderen Fehler gibt, eine Fehlermeldung ausgeben
            raise IOError(f"Fehler beim Laden des Spielstands: {e}")


        
    def saveGame(self):
        with open(self.gameStatePath, 'w') as file0:
            json.dump(self.gameStateContent, file0, indent=1)

    def modelbuilder(self, Modelfile):
        try:
            buildcommand = f"ollama create {self.model} -f {self.modelPath + Modelfile}"
            print("```" + os.popen(buildcommand).read() + "```")
        except Exception as e:
            print(e, "Modelfile nicht gefunden oder invalider Modelname")

    def chat(self, user, content):
        messagehistory = self.gameStateContent
        messagehistory += [{'role': 'user', 'content': f"{user}: {content}"}]
        response = ollama.chat(model=self.model, messages=messagehistory, stream=False)
        messagehistory.append(response['message'])
        answer = response['message']['content']
        self.gameStateContent = messagehistory

        self.saveGame()

        return answer
    


class RPGLoader(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.game = None
        self.channel_id = 1200993669478621226
        self.channel = self.client.get_channel(1200993669478621226)
        self.users = {}
        self.path = os.getcwd()

        self.load_usernames()
        #subprocess.run("./../AI/ollama-linux-amd64 serve", shell=True, capture_output=True, check=True)

    @commands.command(brief="[RPGAI]")
    async def listgames(self, ctx):
        directory_path = self.path + "/modules/main/rpgai/gameStates/"
        try:
            # Überprüfe, ob das Verzeichnis existiert
            if not os.path.exists(directory_path):
                await self.channel.send(f"Fehler: der Pfad {directory_path} existiert nicht")
            # Liste alle Dateien im Verzeichnis auf
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            await self.channel.send(files)
        except Exception as e:
            await self.channel.send(f"Fehler beim Auflisten der Dateien: {e}")

    @commands.command(brief="[RPGAI]")
    async def downloadgame(self, ctx, gameStateName):
        file_path = f'{self.path}/modules/main/rpgai/gameStates/{gameStateName}.txt'
        try:
            with open(file_path, 'rb') as file:
                await ctx.send(content='Hier ist dein GameState:', file=lambda: discord.File(file, filename=f'{gameStateName}.txt'))
        except Exception as e:
            await self.channel.send("Error: ", e)

    @commands.command(brief="[RPGAI]")
    async def loadgame(self, ctx, gameStateName=None):
        
        try:
            self.game = MedievalGame('rpgai')
            self.game.loadGame(gameStateName)
            if gameStateName is None:
                returntext = "Loaded new Game"
            else:
                returntext = f"Loaded {gameStateName}"
        except FileNotFoundError:
            returntext = ("Error: File not found")
        except Exception as e:
            returntext = (f"Error: {e}")

        if isinstance(ctx, discord.DMChannel):
            await ctx.send(returntext)
        else:
            await self.channel.send(returntext)



    @commands.command(brief="[RPGAI]")
    async def savegame(self, ctx, gameStateName):
        game = self.game
        game.loadGame(gameStateName)

        await self.channel.send(game.chat())

    def load_usernames(self):
        try:
            with open("players.json", 'r') as file0:
                self.users = json.load(file0)
        except FileNotFoundError:
            # Falls die Datei nicht gefunden wird, leeres Dictionary initialisieren
            self.users = {}

    @commands.command(brief="[RPGAI] Alle Commands erklärt")
    async def tutorial(self, ctx):
        await self.channel.send('''
Hi du hast das Tutorial aufgerufen!\n
Als allererstes musst du dich zusammen mit einem Owner oder Admin vergewissern, dass dieser Channel über den Bot als Outputchannel für das Game gesetzt wurde.
Falls der Bot schon länger läuft und du schon andere Chats siehst, kannst du diesen Schritt überspringen.\n
Weiterhin musst du einen Usernamen setzen, mit dem du dich in der Game-Welt identifizierst.
Dies kannst du über `.setusername "hier-name"` tun.\n
Falls noch kein Game geladen oder gestartet wurde, kannst du ein neues Spiel mit .loadgame erstellen.
Wenn du ein bestehendes Spiel weiterspielen möchtest, rufe `.listgames` auf.
Dieser Command wird dir eine Liste an gespeicherten Spielen zeigen.
Diese kannst du entweder mit `.downloadgame "hier den namen der txt"` herunterladen oder mit
`.loadgame "hier den namen der txt"` laden.\n
Der nächste Schritt ist in die Welt eintauchen.\n
Du kannst in der Welt spielen in dem du `.chat` oder `.c` aufrufst und dahinter deinen Input für das Spiel schreibst.
            ''')


#######################################################

    @commands.command(aliases=["setuser", "setname"], brief="Hier kannst du deinen Adventurer Namen anpassen!")
    async def setusername(self, ctx, username):
        try:
            with open("players.json", 'r') as file0:
                self.users = json.load(file0)
        except FileNotFoundError:
            # Falls die Datei nicht gefunden wird, leeres Dictionary initialisieren
            self.users = {}

        user_name = ctx.author.name

        if user_name in self.users:
            # Der Benutzer existiert bereits, aktualisiere den Ingame-Namen
            self.users[user_name] = username
        else:
            # Der Benutzer existiert nicht, füge ihn hinzu
            self.users[user_name] = username

        try:
            with open("players.json", 'w') as file0:
                json.dump(self.users, file0, indent=1)
            await self.channel.send(f"Username {username} gesetzt.")
        except Exception as e:
            await self.channel.send(f"Fehler beim Speichern: {e}")


    @commands.command(aliases=["getuser", "getname"],brief="Habe ich einen Adventurer Namen?")
    async def getusername(self, ctx):
        try:
            with open("players.json", 'r') as file0:
                self.users = json.load(file0)
        except FileNotFoundError:
                # Falls die Datei nicht gefunden wird, leeres Dictionary initialisieren
            self.users = {}

        user_name = ctx.author.name

        if user_name in self.users:
            ingame_user = self.users[user_name]
            await self.channel.send(f"Dein Abenteurer heißt {ingame_user}")
        else:
            await self.channel.send("Du hast noch keinen Namen!")

    ############################################################################

    '''@commands.command(aliases=["c"], brief="Mit diesem Befehl und einem Text dahinter interagierst du mit der Spielwelt")
    async def chat(self, ctx, *, message):
        if ctx.author.name in self.users:
            ingameuser = self.users[ctx.author.name]
            await self.channel.send(self.game.chat(ingameuser, message))
        else:
            await self.channel.send("No Ingame Name!")'''

    @commands.Cog.listener()
    async def on_message(self,message):
        if (isinstance(message.channel, discord.channel.DMChannel) or message.channel.id == self.channel_id) and not(message.author.bot):
            if message.content[0] in ["+","-",".","["]:
                return
            elif not any(str(element) in message.content for element in self.get_commands()):
                if message.author.name in self.users:
                    ingameuser = self.users[message.author.name]
                    try:
                        await self.channel.send(self.game.chat(ingameuser, message))
                    except AttributeError as e:
                        await self.loadgame(message.channel)
                        await self.channel.send(self.game.chat(ingameuser, message))
                    except Exception as e:
                        if "httpx.ConnectError: [Errno 111] Connection refused" in e:
                            await self.channel.send(self.game.chat(ingameuser, message))
                else:
                    await self.channel.send("No Ingame Name!")
                

async def setup(client):
    await client.add_cog(RPGLoader(client))

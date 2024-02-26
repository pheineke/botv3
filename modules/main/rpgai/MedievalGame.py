import ollama
from ollama import AsyncClient
import os
import pickle
import json
import asyncio
import random
from datetime import datetime
###########
import discord
from discord.ext import commands

class MedievalGame:
    def __init__(self, model) -> None:
        self.model = model
        self.allModelPath = "./modules/modelFiles/"
        self.gameStateDir = "./modules/gameStates/"

        self.gameStateName = ""
        self.gameStatePath = self.gameStateDir + self.gameStateName

        self.gameStateContent = [{'role': 'system', 'content': 'Messages are given to you like this: "Seraphina : message-conent". You respond to the Adventurers Inputs after his or her Name. In this example, the Adventurer (Which is the Player) named Seraphina says to you "Hi"'}]

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
        else:
            pass

        self.gameStatePath = self.gameStateDir + gameStateName

        try:
            with open(self.gameStatePath, 'r') as file0:
                file = list(json.load(file0))
                self.gameStateContent = file
        except Exception as e:
                with open(self.gameStatePath, 'w') as file0:
                    json.dump(self.gameStateContent, file0)
                with open(self.gameStatePath, 'r') as file0:
                    file = list(json.load(file0))
                    self.gameStateContent = file
        
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

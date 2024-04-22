import random
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

class Card():
    def __init__(self, wert, typ) -> None:
        self.wert = wert
        self.typ = typ
    
    def toString(self):
        return f"{self.wert}-{self.typ}"
    
    def getValue(self):
        if self.wert in "AJQK":
            if self.wert == "A":
                return 11
            return 10
        return int(self.wert)

    def isAce(self):
        return self.wert == "A"
    
class Dealer():
    def __init__(self) -> None:
        self.hiddenCard = None
        self.dealerHand = []
        self.dealerSum = 0
        self.dealerAceCount = 0

        

class Player():
    def __init__(self) -> None:
        self.hiddenCard:Card = None
        self.dealerHand = []
        self.dealerSum = 0
        self.dealerAceCount = 0

class BlackJack(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.deck = []
    

    def buildDeck(self, nmbDecks=1):
        deck = []
        werte = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        typen = ["Herz", "Karo", "Pik", "Kreuz"]

        for i in range(nmbDecks):
            for i in range(werte):
                for j in range(typen):
                    card: Card = Card(werte[i], typen[j])
                    deck.append(card)

    def shuffleDeck(self):
        deckSize = len(self.deck)
        for i in range(deckSize):
            j = random.randint(deckSize)
            currCard = self.deck[i]
            randCard = self.deck[j]
            self.deck[i] = randCard
            self.deck[j] = currCard


    async def startgame(self, interaction: discord.Interaction):
        self.buildDeck(nmbDecks=6)
        self.shuffleDeck()

        dealer = Dealer()
        dealer.hiddenCard:Card = self.deck[(len(self.deck)-1)] # type: ignore
        self.deck.remove(dealer.hiddenCard)
        dealerAceCount += 1 if dealer.hiddenCard.isAce() else 0








async def setup(client):
    await client.add_cog(BlackJack(client))
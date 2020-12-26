import random
from deck import Deck
from player import Player
from card import Card
from enum_helpers import Cards, Actions


class Game:
    def __init__(self, numberOfPlayers):
        self.deck = Deck()
        self.players = []
        for i in range(numberOfPlayers):
            self.createPlayer("Player " + str(i))
        while True:
            self.startTurn()

    def askForAction(self, player):
        player.findTruthfulActions()
        player.showCards()
        player.showCoins()
        print(player.name, "what would you like to do?")
        i = 0
        for action in player.truthful_actions:
            print(Actions(action).name, end = "(" + str(i) + ") ")
            i += 1
        choice = int(input())
        action = player.truthful_actions[choice]
        if action == Actions.tax:
            player.tax()
        elif action == Actions.assassinate:
            print("Which player would you like to assassinate?")
            i = 0
            for player in self.players:
                print(player.name, end=" (" + str(i) + ") ")
                i += 1
            target = self.players[int(input())]
            player.assassinate(target)
        elif action == Actions.steal:
            print("Which player would you like to steal from?")
            i = 0
            for player in self.players:
                print(player.name, end=" (" + str(i) + ") ")
                i += 1
            target = self.players[int(input())]
            player.steal(target)
        elif action == Actions.exchange:
            player.exchange(self.deck)
        elif action == Actions.income:
            player.income()
        elif action == Actions.foreign_aid:
            player.foreignAid()
        elif action == Actions.coup:
            print("Which player would you like to coup?")
            i = 0
            for player in self.players:
                print(player.name, end=" (" + str(i) + ") ")
                i += 1
            target = self.players[int(input())]
            player.coup(target)

    def startTurn(self):
        for player in self.players:
            if player.influence >= 1:
                self.askForAction(player)

    def createPlayer(self, name):
        player = Player(name)

        # give two cards to the player:
        for i in range(2):
            player.giveCard(self.deck.drawFromTop())
        self.players.append(player)

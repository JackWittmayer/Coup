import random
from deck import Deck
from player import Player
from card import Card
from enum_helpers import Cards, Actions, CounterActions, ActionsToCards, CounterActionsToCards
import time


class Game:
    def __init__(self, numberOfPlayers):
        self.deck = Deck()
        self.players = []
        self.remaining_players = []
        for i in range(numberOfPlayers):
            self.createPlayer("Player " + str(i))
        self.showAllCards()
        while True:
            turnResult = self.startTurn()
            if turnResult == 1:
                break

    def askForAction(self, player):
        print()
        print(player.name, "what would you like to do?")
        player.findActions(self.remaining_players)
        player.showCards()
        player.showCoins()
        print()
        player.showTruthfulActions()
        print()
        player.showLieActions()

        choice = int(input())
        action = Actions(choice)
        if action == Actions.tax:
            actionFailed = self.allowChallenges(player, "tax", action, "Duke")
            if not actionFailed:
                player.tax()
        elif action == Actions.assassinate:
            target, choiceInt = self.chooseFromOtherPlayers(player, "assassinate")
            player.coins -= 3
            actionFailed = self.allowChallenges(player, "assassinate", action, target.name)
            if not actionFailed:
                print(target.name, "would you like to block the assassination with a contessa?")
                target.showCards()
                choice = int(input("Yes(0), No(1)"))
                if choice == 0:
                    actionFailed = self.allowChallenges(target, "block assassination",
                                                        CounterActions.block_assassination, "Assassin", isCounterAction=True)
                    if actionFailed:
                        player.assassinate(target)
                if choice == 1:
                    player.assassinate(target)
                if target.influence < 1:
                    self.remaining_players.pop(choiceInt)
        elif action == Actions.steal:
            target, choiceInt = self.chooseFromOtherPlayers(player, "steal from")
            actionFailed = self.allowChallenges(player, "steal from", action, "Captain", target.name)
            if not actionFailed:
                print(target.name, "would you like to block the stealing with a captain or ambassador?")
                target.showCards()
                choice = int(input("Don't block stealing(0), Captain(1), Ambassador(2)"))
                if choice == 1:
                    cardName = "Captain"
                elif choice == 2:
                    cardName = "Ambassador"
                if choice == 1 or choice == 2:
                    actionFailed = self.allowChallenges(target, "block stealing", CounterActions.block_assassination, cardName, isCounterAction=True)
                    if actionFailed:
                        player.steal(target)
                elif choice == 0:
                    player.steal(target)
        elif action == Actions.exchange:
            actionFailed = self.allowChallenges(player, "exchange", action, "Ambassador")
            if not actionFailed:
                player.exchange(self.deck, self.remaining_players)
        elif action == Actions.income:
            player.income()
        elif action == Actions.foreign_aid:
            self.showAllCards()
            print("Would a player like to block foreign aid?")
            choice = int(input("Yes(0), No(1)"))
            if choice == 0:
                blocker, choiceInt = self.chooseFromOtherPlayers(player, "block")
                actionFailed = self.allowChallenges(blocker, "block foreign aid from", CounterActions.block_aid, "Duke", player.name, True)
                if actionFailed:
                    player.foreignAid()
            else:
                player.foreignAid()
        elif action == Actions.coup:
            target, choiceInt = self.chooseFromOtherPlayers(player, "coup")
            player.coup(target)
            if target.influence < 1:
                self.remaining_players.pop(choiceInt)

    def startTurn(self):
        # determine if there is more than one player left:
        self.remaining_players = []
        for player in self.players:
            if player.influence >= 1:
                self.remaining_players.append(player)
        if len(self.remaining_players) == 1:
            print("The game is over.", self.remaining_players[0].name, "won!")
            return 1
        for player in self.remaining_players:
            self.askForAction(player)
        return 0

    def createPlayer(self, name):
        player = Player(name)

        # give two cards to the player:
        for i in range(2):
            player.giveCard(self.deck.drawFromTop())
        self.players.append(player)
        self.remaining_players.append(player)
        player.findActions(self.remaining_players)

    def chooseFromOtherPlayers(self, player, action):
        choiceInt = -1
        i = 0
        if len(self.remaining_players) > 2 or action == "challenge":
            if action == "block":
                print("Which player would like to", action, "?")
            elif action == "challenge":
                print("Would any player like to challenge?")
            else:
                print("Which player would you like to", action + "?")

            if action == "challenge":
                print("No challenge(-1) ", end= "")
            for otherPlayer in self.remaining_players:
                if otherPlayer is player:
                    i += 1
                    continue
                if action == "steal from" and otherPlayer.coins <= 0:
                    i += 1
                    continue
                print(otherPlayer.name, end="(" + str(i) + ") ")
                i += 1
            choiceInt = int(input())
            target = self.remaining_players[choiceInt]

        else:
            i = 0
            for otherPlayer in self.remaining_players:
                if otherPlayer is player:
                    i += 1
                    continue
                target = otherPlayer
                choiceInt = i
                break
        return target, choiceInt

    def allowChallenges(self, player, action_verb, action, cardName, otherPlayerName = "", isCounterAction = False):
        actionFailed = False
        if isCounterAction:
            counterAction = action
            print(player.name, "is attempting to", action_verb, otherPlayerName, "with their", cardName)
        else:
            print(player.name, "is attempting to", action_verb, otherPlayerName, "with their", cardName)

        challenger, choiceInt = self.chooseFromOtherPlayers(player, "challenge")
        if choiceInt == -1:
            return actionFailed
        if not isCounterAction:
            if action not in player.truthful_actions:
                print(player.name, "was caught lying!")
                player.loseInfluence()
                actionFailed = True
            else:
                print(player.name, "was not lying!")
                challenger.loseInfluence()
        else:
            if counterAction not in player.truthful_counter_actions:
                print(player.name, "was caught lying!")
                player.loseInfluence()
                actionFailed = True
            else:
                print(player.name, "was not lying!")
                challenger.loseInfluence()
        return actionFailed

    def showAllCards(self):
        for player in self.players:
            player.showCards()
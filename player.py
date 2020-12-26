from enum_helpers import Actions, CounterActions, Cards
import random
from card import Card

class Player:
    def __init__(self, name):
        self.cards = []
        self.coins = 2
        self.truthful_actions = []
        self.truthful_counter_actions = []
        self.general_actions = [Actions.income, Actions.foreign_aid]
        self.influence = 2
        self.name = name

    def findTruthfulActions(self, remaining_players):
        self.truthful_actions = [Actions.income, Actions.foreign_aid]
        self.truthful_counter_actions = []
        # if player has >= 10 coins, they can only coup:
        if self.coins >= 10:
            self.truthful_actions = [Actions.coup]
            return

        # add all card actions to the lists of truthful actions and counter actions
        for card in self.cards:
            if not card.isDisabled():
                if card.action != -1 and card.action not in self.truthful_actions:
                    # don't add assassinate action if less than 3 coins:
                    if card.action == Actions.assassinate:
                        if self.coins >= 3:
                            self.truthful_actions.append(card.action)
                    elif card.action == Actions.steal:
                        # only add steal action if there is another player with at least 1 coin:
                        validSteal = False
                        for otherPlayer in remaining_players:
                            if otherPlayer is not self and otherPlayer.coins >= 1:
                                validSteal = True
                                break
                        if validSteal:
                            self.truthful_actions.append(card.action)
                    else:
                        self.truthful_actions.append(card.action)
                if card.counter_action != -1 and card.counter_action not in self.truthful_counter_actions:
                    self.truthful_counter_actions.append(card.counter_action)
        # add coup if coins >= 7:
        if self.coins >= 7:
            self.truthful_actions.append(Actions.coup)

    def loseInfluence(self):
        if self.influence == 2:
            print("Which card would you like to lose?")
            lostCard = int(input(self.cards[0].character_string + " (0), " + self.cards[1].character_string + " (1)"))
            self.cards[lostCard].disable()
        elif self.influence == 1:
            print(self.name, "has run out of influence.")
            # disable remaining card:
            for i in range(2):
                if not self.cards[i].isDisabled():
                    self.cards[i].disable()
                    break

        self.influence -= 1

    def giveCard(self, card):
        self.cards.append(card)

    def income(self):
        self.coins += 1

    def foreignAid(self):
        self.coins += 2

    def coup(self, otherPlayer):
        self.coins -= 7
        otherPlayer.loseInfluence()

    def tax(self):
        self.coins += 3

    def steal(self, otherPlayer):
        self.coins += 2
        if CounterActions.block_stealing in otherPlayer.truthful_counter_actions:
            print(otherPlayer.name, "would you like to block the stealing with a captain or ambassador?")
            choice = int(input("Yes(0), No(1)"))
            if choice == 1:
                otherPlayer.getStolenFrom()
        else:
            otherPlayer.getStolenFrom()

    def getStolenFrom(self):
        if self.coins == 1:
            self.coins -= 1
        else:
            self.coins -= 2

    def exchange(self, deck, remaining_players):
        firstCard = deck.drawFromTop()
        secondCard = deck.drawFromTop()
        print("Drawn cards:", firstCard.character_string, ",", secondCard.character_string)
        if self.influence == 2:
            print("Which card or cards would you like to exchange?")
            print(self.cards[0].character_string + "(0) " + self.cards[1].character_string + "(1) " + "Both(2) " + "Neither(3)")
            exchangeCard = int(input())
        elif self.influence == 1:
            print("Would you like to exchange your card?")
            exchangeCard = int(input("Yes(0), No(1)"))
            if exchangeCard == 1:
                exchangeCard = 3
        if exchangeCard == 0 or exchangeCard == 1:
            if self.influence == 2:
                print("Which card would you like to exchange it for?")
                choice = int(input(firstCard.character_string + "(0) " + secondCard.character_string + "(1) "))
                if choice == 0:
                    exchange = self.cards.pop(exchangeCard)
                    self.cards.append(firstCard)
                elif choice == 1:
                    exchange = self.cards.pop(exchangeCard)
                    self.cards.append(secondCard)
            deck.insertCard(exchange)
            self.findTruthfulActions(remaining_players)

        elif exchangeCard == 2:
            deck.insertCard(self.cards.pop())
            deck.insertCard(self.cards.pop())
            self.cards.append(firstCard)
            self.cards.append(secondCard)
            self.findTruthfulActions(remaining_players)

        elif exchangeCard == 3:
            deck.insertCard(firstCard)
            deck.insertCard(secondCard)

        # always reshuffle deck because player saw two cards:
        deck.shuffle()

    def assassinate(self, otherPlayer):
        self.coins -= 3
        if CounterActions.block_assassination in otherPlayer.truthful_counter_actions:
            print(otherPlayer.name, "would you like to block the assassination with a contessa?")
            choice = int(input("Yes(0), No(1)"))
            if choice == 1:
                otherPlayer.loseInfluence()
        else:
            otherPlayer.loseInfluence()

    def showCards(self):
        print("Your cards: ", end= "")
        for card in self.cards:
            if card.isDisabled():
                print("DISABLED: ", end = "")
            print(card.character_string, end=", ")
        print()

    def showCoins(self):
        print("Coins:", str(self.coins))

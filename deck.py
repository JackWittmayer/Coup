# Contains all the cards in the deck, and methods to shuffle, remove cards, etc
import random
from card import Card
from enum_helpers import Cards


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(5):
            for j in range(3):
                card = Card(i)
                self.cards.append(card)
        random.shuffle(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def drawFromTop(self):
        topCard = self.cards.pop()
        return topCard

    def insertCard(self, card):
        self.cards.append(card)
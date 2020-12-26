import enum

class Cards(enum.Enum):
    duke = 0
    assassin = 1
    captain = 2
    ambassador = 3
    contessa = 4

class Actions(enum.Enum):
    tax = 0
    assassinate = 1
    steal = 2
    exchange = 3
    income = 4
    foreign_aid = 5
    coup = 6
    strings = ["Tax", "Assassinate", "Steal", "Exchange", "Income", "Foreign Aid", "Coup"]

    def __getitem__(self, item):
        return self.strings[item]

class CounterActions(enum.Enum):
    block_aid = 0
    block_assassination = 1
    block_stealing = 2


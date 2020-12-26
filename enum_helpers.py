import enum

class Cards(enum.Enum):
    duke = 0
    ambassador = 1
    captain = 2
    assassin = 3
    contessa = 4

class Actions(enum.IntEnum):
    income = 0
    foreign_aid = 1
    tax = 2
    exchange = 3
    steal = 4
    assassinate = 5
    coup = 6

class CounterActions(enum.Enum):
    block_aid = 7
    block_assassination = 8
    block_stealing = 9

class ActionsToCards(enum.Enum):
    duke = Actions.tax
    ambassador = Actions.exchange
    captain = Actions.steal
    assassin = Actions.assassinate

class CounterActionsToCards(enum.Enum):
    duke = CounterActions.block_aid
    ambassador = CounterActions.block_stealing
    contessa = CounterActions.block_assassination


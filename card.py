from enum_helpers import Actions, CounterActions, Cards

class Card:
    def __init__(self, character):
        self.action = -1
        self.counter_action = -1
        self.disabled = False
        self.character = character
        self.character_string = ""
        self.action_string = ""
        self.counter_action_string = ""
        if character == Cards.duke.value:
            self.action = Actions.tax
            self.counter_action = CounterActions.block_aid
            self.character_string = "Duke"
            self.action_string = "Tax"
            self.counter_action_string = "Block Aid"
        elif character == Cards.assassin.value:
            self.action = Actions.assassinate
            self.character_string = "Assassin"
            self.action_string = "Assassinate"
        elif character == Cards.captain.value:
            self.action = Actions.steal
            self.counter_action = CounterActions.block_stealing
            self.character_string = "Captain"
            self.action_string = "Steal"
            self.counter_action_string = "Block Stealing"
        elif character == Cards.ambassador.value:
            self.action = Actions.exchange
            self.counter_action = CounterActions.block_stealing
            self.character_string = "Ambassador"
            self.action_string = "Exchange"
            self.counter_action_string = "Block Stealing"
        elif character == Cards.contessa.value:
            self.counter_action = CounterActions.block_assassination
            self.character_string = "Contessa"
            self.counter_action_string = "Block Assassination"
        else:
            print("Invalid character found:", character)
    
    def disable(self):
        self.disabled = True

    def isDisabled(self):
        return self.disabled

import random

class Set:
    
    def __init__(self, name, description, cards=None, played_cards=None, statistics=None):
        self.name = name
        self.description = description
        self.cards = cards if cards is not None else []
        self.played_cards = played_cards if played_cards is not None else []
        self.statistics = statistics if statistics is not None else {}
    
    def add_card(self, question, answer):
        self.cards.append((question, answer))
        return True
    
    def get_card(self):
        cards_amount = len(self.cards)
        def draw():
            card_num = random.randint(0, cards_amount - 1)
            drawn_card = self.cards.pop(card_num)
            self.played_cards.append(drawn_card)
            return drawn_card
        if cards_amount > 0:
            return draw()
        elif len(self.played_cards) > 0:
            self.cards = self.played_cards
            self.played_cards = []
            cards_amount = len(self.cards)
            return draw()
        else:
            return False
    
    def get_cards(self):
        return self.cards + self.played_cards
    
    def delete_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        if card in self.played_cards:
            self.played_cards.remove(card)
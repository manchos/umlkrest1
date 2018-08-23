import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])

class Frenchdeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

    def spades_heigh(self):
        rank_value = Frenchdeck.ranks.index()

    def __init__(self):
        print(self.ranks)
        print(self.suits)
        self._cards = [
            Card(rank, suit) for suit in self.suits
            for rank in self.ranks]
        print(self._cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]



if __name__ == '__main__':
    beer_card = Card('7', 'diamonds')
    print(beer_card)

    deck = Frenchdeck()
    print(len(deck))

    # for a in [1,2,3]:
    #     for b in ['a','b','c']:
    #         print(a, b)
    #

    print(deck[1])
    print(choice(deck))

    print(Card('Q', 'hearts') in deck)
    print(Card('Q', 'beasts') in deck)


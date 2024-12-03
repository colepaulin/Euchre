import random
from Card import Card
from Player import Player
from typing import List
class Deck:
    """Represents a customizable deck of playing cards."""
    all_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["H", "D", "C", "S"]

    def __init__(self, lower_bound_rank="2"):
        """Creates a deck including only cards ranked at or above the specified lower bound."""
        if lower_bound_rank not in self.all_ranks:
            raise ValueError(f"Invalid rank '{lower_bound_rank}'. Valid ranks are: {', '.join(self.all_ranks)}")
        
        # Find the index of the lower bound and include all ranks above it
        start_index = self.all_ranks.index(lower_bound_rank)
        self.ranks = self.all_ranks[start_index:]

        # Generate cards with the filtered ranks
        self.cards = self.resetCardsAndShuffle()
    
    def resetCardsAndShuffle(self):
        """Resets all cards in the deck to their initial state."""
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def drawCard(self):
        """Draws a card from the deck"""
        return self.cards.pop()
    
    def addCard(self, card):
        """Adds a new card to the deck."""
        self.cards.append(card)
    
    def dealCards(self, cardsPerPlayer: int, order: List[Player]):
        """
        Deals cards to players from the top of the deck.

        :param cardsPerPlayer: the number of cards each player recieves
        :param order: the order to deal the cards
        """
        for player in order:
            player_cards = [self.drawCard() for _ in range(cardsPerPlayer)]
            player.addCards(player_cards)

    def __len__(self):
        """Returns the number of cards left in the deck."""
        return len(self.cards)

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"
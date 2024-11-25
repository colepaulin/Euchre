import random
from Card import Card
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
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def draw_card(self):
        """Draws a card from the deck. Returns None if the deck is empty."""
        return self.cards.pop() if self.cards else None

    def __len__(self):
        """Returns the number of cards left in the deck."""
        return len(self.cards)

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"
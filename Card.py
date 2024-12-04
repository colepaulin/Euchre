class Card:
    """Represents a single playing card."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def equalValue(self, other):
        """Checks if the value of the card is equal to the value of another card."""
        assert isinstance(other, Card)
        return self.rank == other.rank and self.suit == other.suit

    


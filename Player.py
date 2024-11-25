from Card import Card
from Strategy import Strategy
from typing import List

class Player:
    """
    Represents a player in the Euchre game.
    """
    def __init__(self, id: int, strategy: Strategy):
        """
        Initializes a Player instance with a unique identifier and a strategy for gameplay.

        :param id: A unique identifier for the player.
        :param strategy: The strategy the player will use during the game.
        """
        self.id = id
        self.isDealer: bool = False
        self.declaredTrump: bool = False
        self.strategy = strategy
        self.cardsInHand: List[Card] = []
        self.cardsPlayed: List[Card] = []

    def setDealerStatus(self, isDealer: bool):
        """
        Sets the dealer status for the player.

        :param isDealer: Boolean indicating if the player is the dealer.
        """
        self.isDealer = isDealer
    
    def setTrumpStatus(self, declaredTrump: bool):
        """
        Sets the trump declaration status for the player.

        :param declaredTrump: Boolean indicating if the player has declared trump.
        """
        self.declaredTrump = declaredTrump

    def addCards(self, newCards: List[Card]):
        """
        Adds new cards to the player's hand.

        :param newCards: A list of Card objects to be added to the player's hand.
        """
        self.cardsInHand.extend(newCards)
    
    def playCard(self, card: Card):
        """
        Plays a card from the player's hand and updates the player's state accordingly.

        :param card: The card to be played.
        :return: The played card.
        :raises ValueError: If the card is not in the player's hand.
        """
        if card in self.cardsInHand:
            self.cardsInHand.remove(card)
            self.cardsPlayed.append(card)
            return card
        else:
            raise ValueError("The card is not in the player's hand.")
    
    def newHand(self):
        """
        Resets the player's hand and status for a new round.
        """
        self.cardsInHand = []
        self.cardsPlayed = []
        self.declaredTrump = False
        self.isDealer = False

    def __eq__(self, other):
        """
        Checks equality between two Player instances.

        :param other: Another Player instance to compare against.
        :return: True if both players have the same id, dealer status, trump status, and strategy; False otherwise.
        """
        if not isinstance(other, Player):
            return NotImplemented
        return (self.id == other.id and 
                self.isDealer == other.isDealer and 
                self.declaredTrump == other.declaredTrump and 
                self.strategy == other.strategy)

    
    
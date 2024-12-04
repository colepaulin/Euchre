from Card import Card
from typing import List

class Player:
    """
    Represents a player in the Euchre game.
    """
    def __init__(self, id: int, strategy, name: str):
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
        self.isGoingAlone: bool = False
        self.partner: Player
        self.team = None
        self.name = name

    def setTeam(self, team):
        self.team = team
    
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
    
    def setGoingAloneStatus(self, isGoingAlone: bool):
        """
        Sets the going alone status for the player.

        :param isGoingAlone: Boolean indicating if the player is going alone
        """
        self.isGoingAlone = isGoingAlone

    def addCard(self, newCard: Card):
        """
        Adds new card to the player's hand.

        :param newCard: A Card object to be added to the player's hand.
        """
        self.cardsInHand.append(newCard)
    
    def addCards(self, newCards: List[Card]):
        """
        Adds new cards to the player's hand.

        :param newCards: A list of Card objects to be added to the player's hand.
        """
        self.cardsInHand.extend(newCards)
    
    def discard(self):
        """
        Discards a card from the player's hand based on their strategy
        Assumes 1 extra card in player cardsInHand.
        """
        self.strategy.discard(self)

    
    def playCard(self, trumpSuit, leadSuit, teams, handHistory, trickHistory) -> Card:
        """
        Plays a card from the player's hand based on game and strategy

        :param trumpSuit: the trump suit
        :param leadSuit: The lead suit in the trick
        :param teams: A list of the teams
        :param handHistory: see Hand Class
        :param trickHistory: see Trick Class
        """
        return self.strategy.playCard(self,
                                       trumpSuit, 
                                       leadSuit, 
                                       teams, 
                                       handHistory, 
                                       trickHistory)
    
    def passOrPlay(self, teams, faceUpCard, biddingOrder): # faceUpCard is Card | None
        """
        Decision to pass or play in bidding phase based on strategy

        :param teams: list of the teams
        :param faceUpCard: Card that is face up when bidding, None if no face up card
        :param biddingOrder: list of players which represents the bidding order
        :return: True if player plays, false otherwise
        """
        return self.strategy.passOrPlay(self, teams, faceUpCard, biddingOrder)
    
    def chooseTrump(self):
        """
        Player chooses the optimal trump suit in a face down bidding round based on
        their hand
        """
        return self.strategy.chooseTrump(self)

    def shouldGoAlone(self, teams, trumpSuit):
        """
        Decides whether to go alone or not based on the strategy

        :param teams: list of the teams
        :param trumpSuit: The trump suit
        :returns True if going alone, false otherwise
        """
        return self.strategy.shouldGoAlone(self, trumpSuit, teams)
    
    def newHand(self):
        """
        Resets the player's hand and status for a new round.
        """
        self.cardsInHand = []
        self.cardsPlayed = []
        self.declaredTrump = False
        self.isDealer = False
        self.isGoingAlone = False

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

    
    
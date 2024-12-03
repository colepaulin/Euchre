from abc import ABC, abstractmethod
from typing import List
from Card import Card
from Player import Player
from Team import Team

class Strategy(ABC):
    """
    Abstract base class for Euchre playing strategies.
    
    This class defines the interface that all specific strategy implementations
    must follow. Each strategy must implement methods for making key decisions
    during gameplay.
    """
    
    @abstractmethod
    def passOrPlay(self, player: Player, 
                   teams: List[Team], 
                   faceUpCard, # Card | None
                   biddingOrder: List[Player]) -> bool:
        """
        The strategy to pass or play in the bidding stage. A player must know
        the score to the game, if there is a face up card or not, and the bidding order

        :param player: the player making the decision
        :param teams: a list of the teams in the game
        :param faceUpCard: the card that is face up during bidding, None if the card 
                            has been flipped over
        :param biddingOrder: The order that the players are bidding
        :returns True if the player decides to play, False otherwise
        """
        pass

    @abstractmethod
    def chooseTrump(self, player: Player) -> str:
        """
        Player chooses the optimal trump suit in a face down bidding round based on
        their hand
        """
        pass

    @abstractmethod
    def discard(self, player: Player):
        """
        After a dealer picks up a card, they have 6 cards in hand,
        so they must discard 1 card
        :param player: the player making the decision
        modifies cardsInHand
        """
        pass

    @abstractmethod
    def shouldGoAlone(self, player: Player, 
                      trumpSuit, 
                      teams: List[Team]) -> bool:
        """
        Decides whether to go alone or not

        :param player: the player making the decision
        :param trumpSuit: the trump suit of the hand
        :param teams: A list of the teams
        :returns True if the player is going alone, False otherwise
        """
        pass

    @abstractmethod
    def playCard(self, player: Player, 
                 trumpSuit,
                 leadSuit,
                 teams: List[Team],
                 handHistory, 
                 trickHistory) -> Card:
        """
        determine which card to play when it is your turn
        :param player: the player making the decision
        :param trumpSuit: The trump suit in the hand
        :param leadSuit: The leading suit in the trick. None if player is leading
        :param teams: a list of the teams
        :param handHistory: see Hand class
        :param trickHistory: see Trick class
        """
        pass
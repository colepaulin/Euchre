import random
from Strategy import Strategy
from typing import List
from Card import Card
from Player import Player
from Team import Team

class PPOStrategy(Strategy):
    """
    A simple strategy that makes all decisions randomly.
    This can serve as a baseline for comparing other strategies.
    """
    def extractGameState(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         biddingOrder: List[Player],
                         trumpSuit,
                         leadSuit,
                         handHistory,
                         trickHistory):
        pass

    def passOrPlay(self, player: Player, 
                   teams: List[Team], 
                   faceUpCard, #: Card | None, 
                   biddingOrder: List[Player]) -> bool:
        pass


    def discard(self, player: Player):
        pass

    def shouldGoAlone(self, player: Player, 
                      trumpSuit, 
                      teams: List[Team]) -> bool:
        pass
    
    def chooseTrump(self, player: Player):
        pass

    def playCard(self, player: Player, 
                 trumpSuit,
                 leadSuit,
                 teams: List[Team],
                 handHistory, 
                 trickHistory):
        pass
        
        
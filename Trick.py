from typing import List
from Team import Team
from Player import Player
from Card import Card
from Strategy import Strategy
class Trick:
    """
    Represents a singular Trick in Euchre Hand

    Attributes:
        teams: see init
        order: see init
        trumpSuit: see init
        handHistory: see init
        trickHistory: dynamically updates list representing the trick of the form
                            [cardA, cardB, cardC, 0, leadPlayerId]
                      where leadPlayerId plays cardA, then next player plays cardB, ...
                      and 0 represents that the player has not played a card
    """
    def __init__(self, teams: List[Team], order: List[Player], trumpSuit, handHistory):
        """
        :param teams: list of teams
        :param order: order that the players will be playing
        :param trumpSuit: The trump suit
        :param handHistory: The history of the hand
        """
        self.teams = teams
        self.order = order
        self.trumpSuit = trumpSuit
        self.handHistory = handHistory
        self.trickHistory = [0, 0, 0, 0, 0]
    
    def playTrick(self):
        """
        Play a singular trick
        :returns a complete trickHistory
        """
        leadPlayer = self.order[0]
        leadCard: Card = leadPlayer.playCard(self.trumpSuit, None, self.handHistory, self.trickHistory)
        self.trickHistory[0] = leadCard
        self.trickHistory[-1] = leadPlayer.id
        arrIdx = 1
        for player in self.order[1:]:
            playedCard = player.playCard(self.trumpSuit, leadCard.suit, self.handHistory, self.trickHistory)
            self.trickHistory[arrIdx] = playedCard
            arrIdx += 1
        
        return self.trickHistory



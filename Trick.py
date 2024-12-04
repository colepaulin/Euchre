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
    def __init__(self, teams: List[Team], order: List[Player], trumpSuit, handHistory, faceUpCard, faceUp):
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
        self.trickHistory = [-1, -1, -1, -1, -1]
        self.faceUpCard = faceUpCard
        self.faceUp = faceUp
    
    def playTrick(self):
        """
        Play a singular trick
        :returns a complete trickHistory
        """
        leadPlayer = self.order[0]
        if not leadPlayer.partner.isGoingAlone:
            self.trickHistory[-1] = leadPlayer.id
            leadCard: Card = leadPlayer.playCard(self.teams, self.faceUpCard, self.faceUp, 
                                                 self.order,self.trumpSuit, None, 
                                                 self.handHistory, self.trickHistory, self.order)
            self.trickHistory[0] = leadCard
            arrIdx = 1
            for player in self.order[1:]:
                playedCard = player.playCard(self.teams, self.faceUpCard, self.faceUp, 
                                                 self.order,self.trumpSuit, leadCard.suit, 
                                                 self.handHistory, self.trickHistory, self.order)
                self.trickHistory[arrIdx] = playedCard
                arrIdx += 1
        else:
            leadPlayer = self.order[1]
            self.trickHistory[-1] = leadPlayer.id
            self.trickHistory[0] = None
            leadCard: Card = leadPlayer.playCard(self.teams, self.faceUpCard, self.faceUp, 
                                                 self.order,self.trumpSuit, None, 
                                                 self.handHistory, self.trickHistory, self.order)
            self.trickHistory[1] = leadCard
            arrIdx = 2
            for player in self.order[2:]:
                playedCard = player.playCard(self.teams, self.faceUpCard, self.faceUp, 
                                             self.order,self.trumpSuit, leadCard.suit, 
                                             self.handHistory, self.trickHistory, self.order)
                self.trickHistory[arrIdx] = playedCard
                arrIdx += 1
        
        return self.trickHistory



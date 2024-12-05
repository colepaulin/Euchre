from Player import Player
from Card import Card
from typing import List


def determineTrickWinner(trumpSuit: str, leadSuit: str, cardPlayerPairs) -> Player: # : List[(Card, Player)]
    def getComplementSuit(trumpSuit: str) -> str:
        """
        return the suit that is same color as trumpsuit
        """
        if trumpSuit == "H":
            return "D"
        elif trumpSuit == "D":
            return "H"
        elif trumpSuit == "C":
            return "S"
        else: 
            return "C"
    
    def getHigherRank(cardA, cardB) -> Card: # cardA : Card | None
        """
        returns the card with highest absolute rank. If a card is none, the other card wins.
        Both cannot be none
        """
        #assert cardA | cardB  # this assertion was throwing errors *shrug*
        if cardA == None:
            return cardB
        if cardB == None:
            return cardA
        all_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        rankA = all_ranks.index(cardA.rank)
        rankB = all_ranks.index(cardB.rank)
        if rankA > rankB:
            return cardA
        else:
            return cardB
    
    def findBestTrump(trumpCardPairs) -> Player: # trumpCardPairs : List[(Card, Player)]
        """
        return the best card of the trumpcardpairs
        based on Right > Left > Rank
        """
        rightBower = Card("Jack", trumpSuit)
        leftBower = Card("Jack", getComplementSuit(trumpSuit))
        leftPlayer = None
        highCard = None
        highCardPlayer = None

        for (c, p) in trumpCardPairs:
            if c.equalValue(rightBower):
                return p
            if c.equalValue(leftBower):
                leftPlayer = p
            if c.equalValue(getHigherRank(highCard, c)):
                highCard = c
                highCardPlayer = p
        if leftPlayer:
            return leftPlayer
        
        return highCardPlayer

    def findHighestCardPlayer(cardPlayerPairs) -> Player: # cardPlayerPairs : List[(Card, Player)]
        highCard = None
        highPlayer = None
        for (c, p) in cardPlayerPairs:
            if c.equalValue(getHigherRank(highCard, c)):
                highCard = c
                highPlayer = p
        return highPlayer
    
    leftBower = Card("Jack", getComplementSuit(trumpSuit))
    trumpCardPairs = [(card, player) for (card, player) in cardPlayerPairs if card.suit == trumpSuit or card.equalValue(leftBower)]
    if trumpCardPairs:
        return findBestTrump(trumpCardPairs)
    
    leadSuitPairs = [(card, player) for (card, player) in cardPlayerPairs if card.suit == leadSuit and not card.equalValue(leftBower)]
    return findHighestCardPlayer(leadSuitPairs)
    
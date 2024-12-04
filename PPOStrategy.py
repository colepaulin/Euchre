import random
from Strategy import Strategy
from typing import List
from Card import Card
from Player import Player
from Team import Team

cardInd = {"9 of H": 0, "10 of H": 1, "Jack of H": 2, "Queen of H": 3, "King of H": 4, "Ace of H": 5,
            "9 of D": 6, "10 of D": 7, "Jack of D": 8, "Queen of D": 9, "King of D": 10, "Ace of D": 11,
            "9 of C": 12, "10 of C": 13, "Jack of C": 14, "Queen of C": 15, "King of C": 16, "Ace of C": 17,
            "9 of S": 18, "10 of S": 19, "Jack of S": 20, "Queen of S": 21, "King of S": 22, "Ace of S": 23}

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

    def extractBiddingState(self, player: Player, faceUpCard, faceUp, biddingOrder):
        """
        faceUpCard = card object offered for bidding
        faceUp = whether the card is still on the table or open bidding is occurring
        """
        encoding = []
        cardEncoding = [0]*24
        cardEncoding[cardInd[str(faceUpCard)]] = 1
        encoding.extend(cardEncoding)
        
        if faceUp:
            encoding.append(1)
        else:
            encoding.append(0)
        
        orderEncoding = [0]*4
        playerPosition = biddingOrder.index(player)
        orderEncoding[playerPosition] = 1
        encoding.extend(orderEncoding)

        declaredTrumpEncoding = [0]*4
        for p in biddingOrder:
            if p.declaredTrump:
                pPosition = biddingOrder.index(p)
                declaredTrumpEncoding[pPosition] = 1
        encoding.extend(declaredTrumpEncoding)

        return encoding

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
        

# main.py
def main():
    strat = PPOStrategy()
    Cole = Player(0, None, "Cole")
    Jack = Player(1, None, "Jack")
    TGod = Player(2, None, "TGod")
    Chris = Player(3, None, "Chris")
    Chris.declaredTrump = True
    print(strat.extractBiddingState(Jack, Card("10","H"), True, [Cole, Jack, TGod, Chris]))

if __name__ == "__main__":
    main()
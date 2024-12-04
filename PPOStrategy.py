import random
from Strategy import Strategy
from typing import List
from Card import Card
from Player import Player
from Team import Team
from Utils import *

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
                         trickHistory,
                         order):
        def extractScoreInfo(player, teams):
            """
            returns [player euchre score (norm),
                     opponent euchre score (norm),
                     player hand score (norm),
                     opponent hand score (norm)]
            """
            for team in teams:
                if player.id == team.p1.id or player.id == team.p2.id:
                    teamEuchreScore = team.euchreScore
                    teamHandScore = team.handScore
                else:
                    opponentEuchreScore = team.euchreScore
                    opponentHandScore = team.handScore
            euchreScore = [max(teamEuchreScore / 10, 1), max(opponentEuchreScore / 10, 1)]
            handScore = [teamHandScore / 5, opponentHandScore / 5]
            return euchreScore + handScore
        
        def extractTrickInfo(handHistory, trickHistory, order):
            trickInfo = []
            
            for trick in handHistory:
                leadPlayerId = trick[-1]
                leadCard = trick[0]
                trickIdx = 1
                if leadCard == None:
                    leadCard = trick[1]
                    trickIdx = 2
                leadPlayerOrderIdx = order.index(next(player for player in order if player.id == leadPlayerId))
                orderIdx = leadPlayerOrderIdx
                trickInfo.extend(oneHotCardRepresentation(leadCard))
                trickInfo.extend(oneHotPlayerRepresentation(leadPlayerId))
                for _ in range(3):
                    nextPlayer = order[(orderIdx + 1) % 4]
                    orderIdx += 1
                    if trickIdx == 4:
                        nextCard = trick[0]
                        trickIdx += 1
                    else:
                        nextCard = trick[trickIdx]
                        trickIdx += 1
                    trickInfo.extend(oneHotCardRepresentation(nextCard))
                    trickInfo.extend(oneHotPlayerRepresentation(nextPlayer.Id))
            # now handle trick history
            leadTrickPlayer = trickHistory[-1]
            if leadTrickPlayer == -1:
                trickInfo.extend(oneHotCardRepresentation(None))
                trickInfo.extend(oneHotPlayerRepresentation(None))

            leadCard = trickHistory[0]
            trickIdx = 1
            if leadCard == None:
                leadCard = trickHistory[1]
                trickIdx = 2
            leadPlayerOrderIdx = order.index(next(player for player in order if player.id == leadPlayerId))
            orderIdx = leadPlayerOrderIdx
            trickInfo.extend(oneHotCardRepresentation(leadCard))
            trickInfo.extend(oneHotPlayerRepresentation(leadTrickPlayer))
            for _ in range(3):
                nextPlayer = order[(orderIdx + 1) % 4]
                orderIdx += 1
                if trickIdx == 4:
                    nextCard = trickHistory[0]
                    trickIdx += 1
                else:
                    nextCard = trickHistory[trickIdx]
                    trickIdx += 1
                if nextCard == None or nextCard == -1:
                    trickInfo.extend(oneHotCardRepresentation(None))
                else:
                    trickInfo.extend(oneHotCardRepresentation(nextCard))
                trickInfo.extend(oneHotPlayerRepresentation(nextPlayer))
            
            tricksRemaining = 5 - len(handHistory) - 1
            for _ in tricksRemaining:
                for _ in range(4):
                    trickInfo.extend(oneHotCardRepresentation(None))
                    trickInfo.extend(oneHotPlayerRepresentation(None))


        gameInfo = extractScoreInfo(player, teams)
        trickInfo = extractTrickInfo(handHistory, trickHistory, order)

            
        

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
        
        
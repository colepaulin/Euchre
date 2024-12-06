import random
from Strategy import Strategy
from typing import List
from Card import Card
from Player import Player
from Team import Team
from PPO import PPO
from Utils import *
import numpy as np
cardInd = {"9 of H": 0, "10 of H": 1, "Jack of H": 2, "Queen of H": 3, "King of H": 4, "Ace of H": 5,
            "9 of D": 6, "10 of D": 7, "Jack of D": 8, "Queen of D": 9, "King of D": 10, "Ace of D": 11,
            "9 of C": 12, "10 of C": 13, "Jack of C": 14, "Queen of C": 15, "King of C": 16, "Ace of C": 17,
            "9 of S": 18, "10 of S": 19, "Jack of S": 20, "Queen of S": 21, "King of S": 22, "Ace of S": 23}

suitInd = {"H": 0, "D": 1, "S": 2, "C": 3}

class PPOStrategy(Strategy):
    """
    A simple strategy that makes all decisions randomly.
    This can serve as a baseline for comparing other strategies.
    """
    def __init__(self, ppo):
        super().__init__()
        self.ppo: PPO = ppo  # Store the PPO object
    def extractGameState(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         faceUp,
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
            euchreScore = [min(teamEuchreScore / 10, 1), min(opponentEuchreScore / 10, 1)]
            handScore = [teamHandScore / 5, opponentHandScore / 5]
            return euchreScore + handScore
        
        def extractTrickInfo(handHistory, trickHistory, order):
            def oneHotCardRepresentation(card):
                representation = [0]*24
                if card == None or card == -1:
                    return representation
                
                cardIdx = cardInd[str(card)]
                representation[cardIdx] = 1
                return representation

            def oneHotPlayerRepresentation(playerId):
                representation = [0]*4
                if playerId == None:
                    return representation
                representation[playerId] = 1
                return representation
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
                    trickInfo.extend(oneHotPlayerRepresentation(nextPlayer.id))
            # now handle trick history
            validTrick = trickHistory[-1] != -1
            if validTrick:
                leadTrickPlayerId = trickHistory[-1]
                if leadTrickPlayerId == -1:
                    trickInfo.extend(oneHotCardRepresentation(None))
                    trickInfo.extend(oneHotPlayerRepresentation(None))

                leadCard = trickHistory[0]
                trickIdx = 1
                if leadCard == None:
                    leadCard = trickHistory[1]
                    trickIdx = 2
                leadPlayerOrderIdx = order.index(next(player for player in order if player.id == leadTrickPlayerId))
                orderIdx = leadPlayerOrderIdx
                trickInfo.extend(oneHotCardRepresentation(leadCard))
                trickInfo.extend(oneHotPlayerRepresentation(leadTrickPlayerId))
                for _ in range(3):
                    nextPlayeId = order[(orderIdx + 1) % 4].id
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
                    trickInfo.extend(oneHotPlayerRepresentation(nextPlayeId))
                
            tricksRemaining = 5 - len(handHistory) - 1 if validTrick else 5 - len(handHistory)
            for _ in range(tricksRemaining):
                for _ in range(4):
                    trickInfo.extend(oneHotCardRepresentation(None))
                    trickInfo.extend(oneHotPlayerRepresentation(None))
            return trickInfo
        
        def extractBiddingState(player: Player, 
                                faceUpCard, 
                                faceUp, 
                                biddingOrder):
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
            declaredGoingAloneEncoding = [0]*4
            isDealerEncoding = [0]*4
            for p in biddingOrder:
                pPosition = biddingOrder.index(p)
                if p.declaredTrump:
                    declaredTrumpEncoding[pPosition] = 1
                if p.isGoingAlone:
                    declaredGoingAloneEncoding[pPosition] = 1
                if p.isDealer:
                    isDealerEncoding[pPosition] = 1
                    
            encoding.extend(declaredTrumpEncoding)
            encoding.extend(declaredGoingAloneEncoding)
            encoding.extend(isDealerEncoding)

            return encoding

        def extractPlayerInfo(player: Player):
            encoding = []
            handEncoding = [0]*24

            for card in player.cardsInHand:
                handEncoding[cardInd[str(card)]] = 1

            encoding.extend(handEncoding)
            return encoding

        def extractHandInfo(trumpSuit):
            encoding = []
            trumpEncoding = [0]*4
            if trumpSuit:
                trumpEncoding[suitInd[trumpSuit]] = 1
                encoding.extend(trumpEncoding)
                return encoding
            return trumpEncoding
        
        encoding = []
        scoreInfo = extractScoreInfo(player, teams)
        playerInfo = extractPlayerInfo(player)
        biddingInfo = extractBiddingState(player, faceUpCard, faceUp, biddingOrder)
        trickInfo = extractTrickInfo(handHistory, trickHistory, order)
        handInfo = extractHandInfo(trumpSuit)
        encoding.extend(scoreInfo)
        encoding.extend(playerInfo)
        encoding.extend(biddingInfo)
        encoding.extend(trickInfo)
        encoding.extend(handInfo)
        # print("Length of score info:", len(scoreInfo))
        # print("Length of player info:", len(playerInfo))
        # print("Length of bidding info:", len(biddingInfo))
        # print("Length of trick info:", len(trickInfo))
        # print("Length of hand info:", len(handInfo))
        
        return encoding

    def passOrPlay(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         faceUp,
                         biddingOrder: List[Player],
                         trumpSuit,
                         leadSuit,
                         handHistory,
                         trickHistory,
                         order):
        def passPlayActionMask(actionProbs):
            """
            remove unplayable actions
            """
            actionProbsMask = np.zeros_like(actionProbs)
            actionProbsMask[0] = 1
            actionProbsMask[1] = 1
            maskedActionProbs = actionProbs * actionProbsMask
            return maskedActionProbs

        def passPlayActionIdxConv(actionIdx):
            """
            decide to pass or play based on Idx
            """
            if actionIdx == 1:
                return True
            return False

        gameState = self.extractGameState(player, teams, faceUpCard,
                                                 faceUp, biddingOrder, trumpSuit, 
                                                 leadSuit, handHistory, trickHistory, order)
        self.ppo.nextState = gameState
        self.ppo.reward = player.reward
        self.ppo.totalReward += player.reward
        self.ppo.updateMemory()
        player.reward = 0
        actionProbs = self.ppo.predict_action(gameState)
        actionProbsMask = passPlayActionMask(actionProbs)
        actionIdx = self.ppo.sample_action(actionProbsMask)
        self.ppo.state = gameState
        self.ppo.recentAction = actionIdx
        self.ppo.recentActionProb = actionProbs[actionIdx]

        return passPlayActionIdxConv(actionIdx)

    def discard(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         faceUp,
                         biddingOrder: List[Player],
                         trumpSuit,
                         leadSuit,
                         handHistory,
                         trickHistory,
                         order):
        def discardActionMask(actionProbs):
            """
            remove unplayable actions
            """
            actionProbsMask = np.zeros_like(actionProbs)
            actionProbsMask[2] = 1
            actionProbsMask[3] = 1
            actionProbsMask[4] = 1
            actionProbsMask[5] = 1
            actionProbsMask[6] = 1
            actionProbsMask[7] = 1
            maskedActionProbs = actionProbs * actionProbsMask
            return maskedActionProbs
        def discardActionIdxConv(actionIdx, player: Player):
            """
            decide a card to discard based on action idx
            """
            player.cardsInHand.pop(actionIdx - 2)
        gameState = self.extractGameState(player, teams, faceUpCard,
                                                 faceUp, biddingOrder, trumpSuit, 
                                                 leadSuit, handHistory, trickHistory, order)
        self.ppo.nextState = gameState
        self.ppo.reward = player.reward
        self.ppo.totalReward += player.reward
        self.ppo.updateMemory()
        player.reward = 0
        actionProbs = self.ppo.predict_action(gameState)
        actionProbsMask = discardActionMask(actionProbs)
        actionIdx = self.ppo.sample_action(actionProbsMask)
        self.ppo.state = gameState
        self.ppo.recentAction = actionIdx
        self.ppo.recentActionProb = actionProbs[actionIdx]

        discardActionIdxConv(actionIdx, player)

    def shouldGoAlone(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         faceUp,
                         biddingOrder: List[Player],
                         trumpSuit,
                         leadSuit,
                         handHistory,
                         trickHistory,
                         order):
        def shouldGoAloneActionMask(actionProbs):
            """
            remove unplayable actions
            """
            actionProbsMask = np.zeros_like(actionProbs)
            actionProbsMask[8] = 1
            actionProbsMask[9] = 1
            maskedActionProbs = actionProbs * actionProbsMask
            return maskedActionProbs
        
        def shouldGoAloneActionIdxConv(actionIdx):
            """
            decide to go alone or not based on actionIdx
            """
            if actionIdx == 8:
                return True
            return False
        
        gameState = self.extractGameState(player, teams, faceUpCard,
                                                 faceUp, biddingOrder, trumpSuit, 
                                                 leadSuit, handHistory, trickHistory, order)
        self.ppo.nextState = gameState
        self.ppo.reward = player.reward
        self.ppo.totalReward += player.reward
        self.ppo.updateMemory()
        player.reward = 0
        actionProbs = self.ppo.predict_action(gameState)
        actionProbsMask = shouldGoAloneActionMask(actionProbs)
        actionIdx = self.ppo.sample_action(actionProbsMask)
        self.ppo.state = gameState
        self.ppo.recentAction = actionIdx
        self.ppo.recentActionProb = actionProbs[actionIdx]

        return shouldGoAloneActionIdxConv(actionIdx)
    
    def chooseTrump(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         faceUp,
                         biddingOrder: List[Player],
                         trumpSuit,
                         leadSuit,
                         handHistory,
                         trickHistory,
                         order):
        def chooseTrumpActionMask(actionProbs, faceUpCard):
            """
            remove unplayable actions
            """
            unavailableSuit = faceUpCard.suit
            actionProbsMask = np.zeros_like(actionProbs)
            actionProbsMask[10] = 1 if "H" != unavailableSuit else 0
            actionProbsMask[11] = 1 if "D" != unavailableSuit else 0
            actionProbsMask[12] = 1 if "S" != unavailableSuit else 0
            actionProbsMask[13] = 1 if "C" != unavailableSuit else 0
            maskedActionProbs = actionProbs * actionProbsMask
            return maskedActionProbs
            
        def chooseTrumpActionIdxConv(actionIdx):
            """
            decide trump
            """
            if actionIdx == 10:
                return "H"
            elif actionIdx == 11:
                return "D"
            elif actionIdx == 12:
                return "S"
            else:
                return "C"
        gameState = self.extractGameState(player, teams, faceUpCard,
                                                 faceUp, biddingOrder, trumpSuit, 
                                                 leadSuit, handHistory, trickHistory, order)
        self.ppo.nextState = gameState
        self.ppo.reward = player.reward
        self.ppo.totalReward += player.reward
        self.ppo.updateMemory()
        player.reward = 0
        actionProbs = self.ppo.predict_action(gameState)
        actionProbsMask = chooseTrumpActionMask(actionProbs, faceUpCard)
        actionIdx = self.ppo.sample_action(actionProbsMask)
        self.ppo.state = gameState
        self.ppo.recentAction = actionIdx
        self.ppo.recentActionProb = actionProbs[actionIdx]

        return chooseTrumpActionIdxConv(actionIdx)
    
    def playCard(self, player: Player,
                         teams: List[Team],
                         faceUpCard,
                         faceUp,
                         biddingOrder: List[Player],
                         trumpSuit,
                         leadSuit,
                         handHistory,
                         trickHistory,
                         order):
        def PlayCardActionMask(actionProbs, player, leadSuit):
            """
            remove unplayable actions
            """
            actionProbsMask = np.zeros_like(actionProbs)
            if player.partner.isGoingAlone:
                actionProbsMask[19] = 1
                maskedActionProbs = actionProbs * actionProbsMask
                return maskedActionProbs
            
            if leadSuit:
                matching_card_indices = [index for index, card in enumerate(player.cardsInHand) if card.suit == leadSuit]
                if matching_card_indices:
                    for cardIdx in matching_card_indices:
                        actionProbsMask[cardIdx+14] = 1
                    maskedActionProbs = actionProbs * actionProbsMask
                    return maskedActionProbs
            
            actionProbsMask[14] = 1 if len(player.cardsInHand) >= 1 else 0
            actionProbsMask[15] = 1 if len(player.cardsInHand) >= 2 else 0
            actionProbsMask[16] = 1 if len(player.cardsInHand) >= 3 else 0
            actionProbsMask[17] = 1 if len(player.cardsInHand) >= 4 else 0
            actionProbsMask[18] = 1 if len(player.cardsInHand) >= 5 else 0
            maskedActionProbs = actionProbs * actionProbsMask
            return maskedActionProbs
        
        def playCardActionIdxConv(actionIdx):
            """
            decide card to play based on actionIdx
            """
            if actionIdx == 19:
                return None
            chosen_card = player.cardsInHand[actionIdx-14]
            player.cardsInHand.remove(chosen_card)
            player.cardsPlayed.append(chosen_card)
            return chosen_card
        if not player.partner.isGoingAlone:
            gameState = self.extractGameState(player, teams, faceUpCard,
                                                    faceUp, biddingOrder, trumpSuit, 
                                                    leadSuit, handHistory, trickHistory, order)
            self.ppo.nextState = gameState
            self.ppo.reward = player.reward
            self.ppo.totalReward += player.reward
            self.ppo.updateMemory()
            player.reward = 0

            actionProbs = self.ppo.predict_action(gameState)
            actionProbsMask = PlayCardActionMask(actionProbs, player, leadSuit)
            actionIdx = self.ppo.sample_action(actionProbsMask)
            self.ppo.state = gameState
            self.ppo.recentAction = actionIdx
            self.ppo.recentActionProb = actionProbs[actionIdx]
            return playCardActionIdxConv(actionIdx)
        else:
            return None

# main.py
def main():
    strat = PPOStrategy()
    Cole = Player(0, None, "Cole")
    Jack = Player(1, None, "Jack")
    TGod = Player(2, None, "TGod")
    Chris = Player(3, None, "Chris")

if __name__ == "__main__":
    main()
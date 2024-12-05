import random
from Strategy import Strategy
from typing import List
from Card import Card
from Player import Player
from Team import Team
from Utils import getLowerRank, getHigherRank
cardInd = {"9 of H": 0, "10 of H": 1, "Jack of H": 2, "Queen of H": 3, "King of H": 4, "Ace of H": 5,
            "9 of D": 6, "10 of D": 7, "Jack of D": 8, "Queen of D": 9, "King of D": 10, "Ace of D": 11,
            "9 of C": 12, "10 of C": 13, "Jack of C": 14, "Queen of C": 15, "King of C": 16, "Ace of C": 17,
            "9 of S": 18, "10 of S": 19, "Jack of S": 20, "Queen of S": 21, "King of S": 22, "Ace of S": 23}

suitInd = {"H": 0, "D": 1, "S": 2, "C": 3}
class GreedyStrategy(Strategy):
    """
    A simple strategy that makes all decisions randomly.
    This can serve as a baseline for comparing other strategies.
    """
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
        """
        randomly decide to pass or play. 
        :returns True if Play, false otherwise
        """
        numTrumps = sum(1 for card in player.cardsInHand if card.suit == faceUpCard.suit)
        if numTrumps >= 2:
            return True
        return False

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
        toDiscard = None
        for card in player.cardsInHand:
            # throw lowest non-trump
            if card.suit == trumpSuit and toDiscard == None: # Must select if not card selected, even tho trump
                toDiscard = card
            elif card.suit == trumpSuit and toDiscard != None: # already have a "best" card
                if toDiscard.suit == trumpSuit:
                    toDiscard = getLowerRank(toDiscard, card) # select lowest of trump cards
                # else we will still want to throw discard as it is nontrump
            elif card.suit != trumpSuit and toDiscard == None:
                toDiscard = card
            else: # card is not trump and current discard exists
                if toDiscard.suit == trumpSuit:
                    toDiscard = card
                else:
                    toDiscard = getLowerRank(card, toDiscard)
        
        if toDiscard:
            player.cardsInHand.remove(toDiscard)
            player.cardsPlayed.append(toDiscard)

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
        numTrumps = sum(1 for card in player.cardsInHand if card.suit == faceUpCard.suit)
        if numTrumps >= 4:
            return True
        return False
    
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
        suit_counts = {"H": 0, "D": 0, "C": 0, "S": 0}
        for card in player.cardsInHand:
            suit_counts[card.suit] += 1
        most_common_suit = max(suit_counts, key=suit_counts.get)
        return most_common_suit

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
        """
        Randomly select a legal card to play from hand.
        Must follow suit if possible.
        """
        if player.partner.isGoingAlone:
            return None
        # If a suit was led, must follow suit if possible
        if leadSuit:
            matching_cards = [card for card in player.cardsInHand if card.suit == leadSuit]
            if matching_cards:
                chosenCard = None
                for card in matching_cards:
                    chosenCard = getHigherRank(chosenCard, card)
                player.cardsInHand.remove(chosenCard)
                player.cardsPlayed.append(chosenCard)
                return chosenCard
        

        
        # If no matching cards or no lead suit, can play any card
        trump_cards = [card for card in player.cardsInHand if card.suit == trumpSuit]
        chosenCard = None
        if trump_cards:
            for card in trump_cards:
                chosenCard = getHigherRank(chosenCard, card)
        else:
            for card in player.cardsInHand:
                chosenCard = getHigherRank(chosenCard, card)
        player.cardsInHand.remove(chosenCard)
        player.cardsPlayed.append(chosenCard)
        return chosenCard
        
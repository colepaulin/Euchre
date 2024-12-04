import random
from Strategy import Strategy
from typing import List
from Card import Card
from Player import Player
from Team import Team

class RandomStrategy(Strategy):
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
        pass

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
        return random.choice([True, False])


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
        if player.cardsInHand:
            card_to_discard = random.choice(player.cardsInHand)
            player.cardsInHand.remove(card_to_discard)

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
        return random.choice([True, False])
    
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
        return random.choice(['H','C','S','D'])

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
                chosen_card = random.choice(matching_cards)
                player.cardsInHand.remove(chosen_card)
                return chosen_card
        
        # If no matching cards or no lead suit, can play any card
        chosen_card = random.choice(player.cardsInHand)
        player.cardsInHand.remove(chosen_card)
        player.cardsPlayed.append(chosen_card)
        return chosen_card
        
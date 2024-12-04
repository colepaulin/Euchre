from Player import Player
from Trick import Trick
from Deck import Deck
from Card import Card
from Bidding import Bidding
from typing import List
from Utils import determineTrickWinner
from Team import Team

GOING_ALONE_MARCH_SCORE = 4
MARCH_SCORE = 2
EUCHRE_SCORE = 2
MAJORITY_TRICK_SCORE = 1

class Hand:
    """
    Represents a hand in Euchre. A hand is made up of bidding, then 5 tricks. 
    Each hand is in charge of reshuffling the cards and dealing them.

    Attributes:
        trumpSuit: the declared trump suit
        order: list of players in their turn order. This can be adjusted in bidding phase
                and trick phase
        faceUpCard: the face up card during the bidding stage
        handHistory: List of trick histories.
                    each trick history is of the form
                            [CardA, CardB, CardC, cardD, leadPlayerId]
                    where CardA is the first card played, then cardB, etc
        recentTrick: The most recent trick of format shown above
    """
    def __init__(self, order: List[Player], teams: List[Team], deck: Deck, cardsPerPlayer: int = 5):
        """
        shuffles the deck of cards and deals them to start new hand

        :param order: list of players in their turn order.
        :param teams: list of the 2 teams
        :param deck: the deck of playing cards
        :param cardsPerPlayer: the number of cards to deal each person (default 5)
        """
        self.cardsPerPlayer = cardsPerPlayer
        self.trumpSuit = None
        self.order = order
        self.teams = teams
        self.deck = deck
        self.deck.resetCardsAndShuffle() 
        self.dealCards()
        self.faceUpCard: Card = self.deck.drawCard()
        self.handHistory = []
        self.recentTrick = []
    
    def playHand(self):
        """
        Each hand consists of a bidding phase, then the tricks.
        It them calculates hand score into a euchre score. It then resets 
        both teams' hand. Updates the teams Euchre points by updating Team 
        attribute
        """
        self.biddingPhase()
        self.playTricks()
        self.handToEuchreScoreConv()
        for team in self.teams:
            team.resetHand()
    
    def dealCards(self):
        """
        Deal the deck of cards accoding to the order
        """
        self.deck.dealCards(self.cardsPerPlayer, self.order)
    
    def biddingPhase(self):
        """
        play the bidding phase. It should be based on the score, the order,
        the face up card, and the cards in the players hand. Updates
        all necessary attributes dynamically
        """
        # TODO FIX TO INCORPORATE BIDDING
        # bidding.run(self.faceUpCard, self.order)
        bidding = Bidding(self.faceUpCard, self.order, self.teams)
        bidding.run()
        self.trumpSuit = bidding.trump
        if bidding.goAloneGuy:
            bidding.goAloneGuy.isGoingAlone = True
            partner = bidding.goAloneGuy.partner
            partner.cardsInHand = [Card("2","H"),Card("2","H"),Card("2","H"),Card("2","H"),Card("2","H")]# TODO clean this up
            # ^ assumes 2 of Hearts is unused and there are 5 tricks
            # self.order.remove(bidding.goAloneGuy.partner) CAN'T REMOVE PERSON FROM ORDER
    
    def playTricks(self):
        """
        Plays a trick for each card in hand (typically 5 for Euchre). 
        After each trick, update the handHistory
        """
        for round in range(self.cardsPerPlayer):
            trick = Trick(self.teams, self.order, self.trumpSuit, self.handHistory)
            self.recentTrick = trick.playTrick()
            self.handHistory.append(self.recentTrick)
            self.updateOrderAndPoints()
    
    def updateOrderAndPoints(self):
        """
        Update the order based on the previous trick.
        Whichever player won the previous trick will go first. 
        The rotation order will stay the same
        """
        winner = self.trickWinner()
        winnerIndex = next(i for i, p in enumerate(self.order) if p.id == winner.id)
        self.order = self.order[winnerIndex:] + self.order[:winnerIndex]
        for team in self.teams:
            if team.p1.id == winner.id or team.p2.id == winner.id:
                team.addHandPoints(1)
        

    def trickWinner(self) -> Player:
        """
        Determine the winner of the most recent trick.

        Returns:
            Player: The player who won the trick
        """
        leadCard = self.recentTrick[0]
        leadSuit = leadCard.suit
        leadPlayerId = self.recentTrick[-1]
        
        # Find the lead player's position in the order
        leadPlayerIndex = next(i for i, p in enumerate(self.order) if p.id == leadPlayerId)
        
        # Map cards to their players in play order
        cards_played = self.recentTrick[:-1]  # Get just the cards
        player_indices = [(leadPlayerIndex + i) % 4 for i in range(4)]  # Get indices in play order
        print(str([cards_played,player_indices]))
        for team in self.teams:
            if team.isGoingAlone():
                print("someone on " + team.name + " went alone\n")
        card_player_pairs = list(zip(cards_played, [self.order[i] for i in player_indices]))        
        return determineTrickWinner(self.trumpSuit, leadSuit, card_player_pairs)

    def handToEuchreScoreConv(self):
        """
        Converts the score of the hand to a Euchre score
        Rules:
            trump declaring team scores as follows
                5 hands and going alone   : +4
                5 hands (march)           : +2
                3 <= hands < 5 (majority) : +1
            nontrump declaring team scores as follows
                >= 3 hands                : +2
        
        Adds euchre points to each team dynamically
        """
        team1: Team = self.teams[0]
        team2: Team = self.teams[1]
        trumpTeam: Team = team1 if team1.declaredTrump else team2
        nonTrumpTeam: Team = team2 if team1 == trumpTeam else team1
        trumpTeamScore: int = trumpTeam.handScore

        if trumpTeamScore == 5 and trumpTeam.isGoingAlone():
            trumpTeam.addEuchrePoints(GOING_ALONE_MARCH_SCORE)

        elif trumpTeamScore == 5:
            trumpTeam.addEuchrePoints(MARCH_SCORE)
        
        elif trumpTeamScore >= 3:
            trumpTeam.addEuchrePoints(MAJORITY_TRICK_SCORE)
        
        else:
            nonTrumpTeam.addEuchrePoints(EUCHRE_SCORE)
            


        

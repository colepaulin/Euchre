from Player import Player
from Trick import Trick
from Deck import Deck
from Card import Card
from Bidding import Bidding
from typing import List
from Team import Team

GOING_ALONE_MARCH_SCORE = 4
MARCH_SCORE = 2
EUCHRE_SCORE = 2
MAJORITY_TRICK_SCORE = 1

class Hand:
    def __init__(self, order: List[Player], teams: List[Team], deck: Deck, cardsPerPlayer: int = 5):
        self.cardsPerPlayer = cardsPerPlayer
        self.trump = None
        self.order = order
        self.teams = teams
        self.tricks: List[Trick] = [Trick() for _ in range(self.cardsPerPlayer)] # TODO trick initialization
        deck.resetCardsAndShuffle() 
        self.dealCards()
        self.faceUpCard: Card = deck.drawCard()
    
    def playHand(self):
        self.biddingPhase()
        self.playTricks()
        self.handToEuchreScoreConv()
        self.resetTeamInfo()
    
    def dealCards(self, deck: Deck):
        deck.dealCards(self.cardsPerPlayer, self.order)
    
    def biddingPhase(self):
        # TODO FIX TO INCORPORATE BIDDING
        # bidding.run(self.faceUpCard, self.order)
    
    def playTricks(self):
        for trick in self.tricks:
            trick.play() # NOTE must update the team.handScore
    
    def handToEuchreScoreConv(self):
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
        
    def resetTeamInfo(self):
        for team in self.teams:
            team.resetHand()
            


        

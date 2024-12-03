from Team import Team
from Hand import Hand
from Deck import Deck
import random

class Euchre:
    """
    Represents a game of Euchre
    """
    def __init__(self, 
                 t1: Team, 
                 t2: Team, 
                 lowBoundCardRank: int = 9, 
                 cardsPerPlayer: int = 5):
        """
        Start a game of Euchre with 2 teams. The starting order
        is randomly initialized
        :param t1: one team in the game
        :param t2: another team in the game
        :param lowBoundCardRank: the lowest rank card included in the deck
        :param cardsPerPlayer: Is the cards each player gets per hand
        """
        self.t1 = t1
        self.t2 = t2
        self.teams = [self,t1, self.t2]
        self.deck = Deck(lowBoundCardRank)
        self.order = self.initializeOrder()
        self.cardsPerPlayer = cardsPerPlayer
    
    def initializeOrder(self):
        """
        Randomize an order that alternates players on different teams
        :returns an order of players of form List[Player]
        """
        order = [random.choice([self.t1.p1, self.t1.p2]), random.choice([self.t2.p1, self.t2.p2])]
        for team in [self.t1, self.t2]:
            for player in [team.p1, team.p2]:
                if player not in order:
                    order.append(player)
        return order
    
    def playEuchre(self):
        """
        Simulate the Game of Euchre. Play a hand then check for winner

        :returns the winning team
        """
        while True:
            self.playNewHand()
            winner = self.checkWinner()
            if winner:
                print(f"Game over! {winner.name} wins with a score of {winner.euchreScore}!")
                return winner
    
    def playNewHand(self):
        """
        plays a hand based on the Hand Class
        """
        hand: Hand = Hand(self.order, self.teams, self.deck, self.cardsPerPlayer)
        hand.playHand()
        
    def checkWinner(self):
        """
        :returns the winning team, or False if there is no winner
        """
        if self.t1.euchreScore >= 10:
            return self.t1
        elif self.t2.euchreScore >= 10:
            return self.t2
        else:
            return False

        
from Team import Team
from Hand import Hand
import random

class Euchre:
    def __init__(self, t1: Team, t2: Team):
        self.t1 = t1
        self.t2 = t2
        self.order = self.initializeOrder()
    
    def initializeOrder(self):
        order = [random.choice([self.t1.p1, self.t1.p2]), random.choice([self.t2.p1, self.t2.p2])]
        for team in [self.t1, self.t2]:
            for player in [team.p1, team.p2]:
                if player not in order:
                    order.append(player)
        return order
    
    def playNewHand(self):
        
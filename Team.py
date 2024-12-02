from Player import Player

class Team:
    """
    Represents a team in the Euchre game, consisting of two players.
    """
    def __init__(self, p1: Player, p2: Player):
        """
        Initializes a Team instance with two Player objects and sets the initial state of calledTrump to False.

        :param p1: The first player in the team.
        :param p2: The second player in the team.
        """
        self.p1 = p1
        self.p2 = p2
        self.declaredTrump: bool = False
        self.score: int = 0
    
    def setTrumpStatus(self, declaredTrump: bool):
        """
        updates if a team declared trump or not

        :param declaredTrump: whether or not the team declared trump
        """
        self.declaredTrump = declaredTrump
    
    def addPoints(self, addedPoints: int):
        self.score += addedPoints
    
    def reset(self):
        self.score = 0
        self.declaredTrump = False
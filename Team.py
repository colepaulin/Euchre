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
        self.euchreScore: int = 0
        self.handScore: int = 0
    
    def setTrumpStatus(self, declaredTrump: bool):
        """
        updates if a team declared trump or not

        :param declaredTrump: whether or not the team declared trump
        """
        self.declaredTrump = declaredTrump
    
    def addEuchrePoints(self, addedPoints: int):
        """
        add Euchre points (overall game score)
        """
        self.euchreScore += addedPoints
    
    def addHandePoints(self, addedPoints: int):
        """
        add Hand points (points in a specific hand)
        """
        self.handScore += addedPoints
    
    def isGoingAlone(self):
        """
        test to see if the team is going alone
        """
        return self.p1.isGoingAlone or self.p2.isGoingAlone
    
    def resetHand(self):
        """
        used to reset each players hand and reset the hand score and set declared
        trump to false
        """
        self.handScore = 0
        self.declaredTrump = False
        self.p1.newHand()
        self.p2.newHand()

    
    def resetEuchre(self):
        """
        reset the game of euchre
        """
        self.euchreScore = 0
        self.declaredTrump = False

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
        self.calledTrump: bool = False
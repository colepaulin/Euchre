from Player import Player
from typing import List

class Hand:
    def __init__(self, order: List[Player]):
        self.trump = None
        self.order = order


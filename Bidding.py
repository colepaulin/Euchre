from Card import Card
from Player import Player
from Team import Team
from typing import List

class Bidding:
    def __init__(self, card: Card, order: List[Player], teams: List[Team], faceUp = True):
        self.card = card
        self.order = order
        self.teams = teams
        self.faceUp = faceUp
        self.trump = None
        self.goAloneGuy = None

    def run(self):
        """
        Run through the entire bidding phase, iterating through the players in their
        given bidding order (passed down from Hand), and they decide what to do based
        on their strategy
        """
        for player in self.order: # first round (face up card)
            if player.passOrPlay(self.teams, self.card, self.faceUp, self.order,
                                 None, None, [], [-1], self.order):
                dealer = self.order[-1]
                dealer.addCard(self.card) # add that card to the DEALER'S hand
                self.trump = self.card.suit
                player.declaredTrump = True
                player.team.declaredTrump = True
                dealer.discard(self.teams, self.card, self.faceUp, self.order,
                                 self.trump, None, [], [-1], self.order)
                
                # make modular
                if player.shouldGoAlone(self.teams, self.card, self.faceUp, self.order,
                                        self.trump, None, [], [-1], self.order):
                    self.goAloneGuy = player
                else:
                    for team in self.teams:
                        if team.p1 == player:
                            partner = team.p2
                        elif team.p2 == player:
                            partner = team.p1
                    if partner.shouldGoAlone(self.teams, self.card, self.faceUp, self.order,
                                            self.trump, None, [], [-1], self.order):
                        self.goAloneGuy = partner

                return None # exit bidding
        
        self.faceUp = False # might be redundant if we just pass None into the card argument anyways
        for player in self.order: # second round (face down card)
            if player.passOrPlay(self.teams, self.card, self.faceUp, self.order,
                                    None, None, [], [-1], self.order):
                self.trump = player.chooseTrump(self.teams, self.card, self.faceUp, self.order,
                                    None, None, [], [-1], self.order)
                player.declaredTrump = True
                player.team.declaredTrump = True

                if player.shouldGoAlone(self.teams, self.card, self.faceUp, self.order,
                                        self.trump, None, [], [-1], self.order): # logic for going alone
                    self.goAloneGuy = player
                else:
                    for team in self.teams:
                        if team.p1 == player:
                            partner = team.p2
                        elif team.p2 == player:
                            partner = team.p1
                    if partner.shouldGoAlone(self.teams, self.card, self.faceUp, self.order,
                                            self.trump, None, [], [-1], self.order):
                        self.goAloneGuy = partner

                return None # exit bidding
        
        if self.trump == None: # dealer is screwed
            dealer = self.order[-1]
            self.trump = dealer.chooseTrump(self.teams, self.card, self.faceUp, self.order,
                                            None, None, [], [-1], self.order)
            dealer.declaredTrump = True
            dealer.team.declaredTrump = True
            
            if dealer.shouldGoAlone(self.teams, self.card, self.faceUp, self.order,
                                    self.trump, None, [], [-1], self.order): # logic for going alone
                    self.goAloneGuy = dealer
            else:
                for team in self.teams:
                    if team.p1 == dealer:
                        partner = team.p2
                    elif team.p2 == dealer:
                        partner = team.p1
                if partner.shouldGoAlone(self.teams, self.card, self.faceUp, self.order,
                                            self.trump, None, [], [-1], self.order):
                    self.goAloneGuy = partner
            
            return None # exit bidding
from Team import Team
from Hand import Hand
from Deck import Deck
from Player import Player
from RandomStrategy import RandomStrategy
from PPOStrategy import *
import random

from torch import torch
from torch.optim import Adam

class Euchre:
    """
    Represents a game of Euchre
    """
    def __init__(self, 
                 t1: Team, 
                 t2: Team, 
                 lowBoundCardRank: str = "9", 
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
        self.teams = [self.t1, self.t2]
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
        """

        while True:
            self.playNewHand()
            winner = self.checkWinner()
            self.order = self.order[1:] + [self.order[0]]
            if winner:
                winner.p1.reward = 100
                winner.p2.reward = 100
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
        
    def calculate_reward(self, player):
        pass

    def step(self, player, action):
        """
        Processes the action taken by a specific player and updates the game state.

        Args:
            player: The player taking the action.
            action: The action taken by the player (e.g., card played, bid made).

        Returns:
            next_state: The updated game state after the action.
            reward: The reward for the acting player.
            done: Boolean indicating if the game (or hand) is over.
        """
        # 1. apply an action
        # 2. compute reward for acting player
        # 3. check if the game or phase is over
        # 4. return the updated state, reward, and done flag

        # in the training loop, make sure to loop through this step function for each player
        pass
        
# main.py
def main():
    print("Hello, World!")
    Cole = Player(0, RandomStrategy(), "Cole")
    Jack = Player(1, RandomStrategy(), "Jack")
    TGod = Player(2, RandomStrategy(), "TGod")
    Chris = Player(3, RandomStrategy(), "Chris")

    Republicans = Team(Cole, Jack, "Republicans")
    Democrats = Team(TGod, Chris, "Democrats")

    game = Euchre(Republicans, Democrats, )
    game.playEuchre()

    '''
    EXAMPLE GAME LOOP
    
    # Initialize model, optimizer, and agent
    input_dim = 300  # Adjust based on game state encoding size
    action_dim = 24  # Number of possible actions (cards)
    model = EuchrePPOModel(input_dim, action_dim)
    optimizer = Adam(model.parameters(), lr=1e-4)
    agent = PPOAgent(model, optimizer, action_dim)

    # Training loop
    for episode in range(1000):
        state = game.reset()
        done = False
        states, actions, rewards, log_probs, dones = [], [], [], [], []

        while not done:
            state_tensor = torch.tensor(state, dtype=torch.float32)
            logits, _ = model(state_tensor)
            action_probs = torch.softmax(logits, dim=-1)
            action = torch.multinomial(action_probs, 1).item()

            # Take the action in the game
            next_state, reward, done = game.step(action)

            # Log data for PPO
            states.append(state_tensor)
            actions.append(action)
            rewards.append(reward)
            log_probs.append(torch.log(action_probs[action]))
            dones.append(done)

            state = next_state

        # Update the PPO agent
        agent.update(states, actions, log_probs, rewards, dones)
    '''


if __name__ == "__main__":
    main()
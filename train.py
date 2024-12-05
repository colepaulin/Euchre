from Player import Player
from Team import Team
from RandomStrategy import RandomStrategy
from PPOStrategy import PPOStrategy
from Euchre import Euchre
from PPO import PPO
import torch
import torch.nn as nn
import numpy as np

# Initialize PPO Strategy
state_dim = 633  # State vector size
action_dim = 19  # Action space size (e.g., number of cards in hand) TODO
ppo = PPO(state_dim=state_dim, action_dim=action_dim)  # Your PPO model

def initializeNewEuchre(ppo):
    # Initialize Players
    player1 = Player(0, PPOStrategy(ppo), "PPO_Player")
    player2 = Player(1, RandomStrategy(), "Rand1_partner")
    player3 = Player(2, RandomStrategy(), "Rand2_opp")
    player4 = Player(3, RandomStrategy(), "Rand3_opp")

    # Set up teams
    team1 = Team(player1, player2, "Team1")
    team2 = Team(player3, player4, "Team2")

    # Initialize the game
    game = Euchre(team1, team2)
    return game

def train_ppo(ppo, num_games=1000):
    for game_num in range(num_games):
        print(f"Starting game {game_num + 1}")
        
        # Initialize game
        game = initializeNewEuchre(ppo)
        game.playEuchre()

        # After the game, update PPO with collected memory
        ppo.update()

        # Optional: Save the model periodically
        if (game_num + 1) % 100 == 0:
            torch.save(ppo.actor.state_dict(), f"ppo_actor_{game_num + 1}.pth")
            torch.save(ppo.critic.state_dict(), f"ppo_critic_{game_num + 1}.pth")
            print(f"Model saved at game {game_num + 1}.")

# Train the model
train_ppo(ppo, num_games=1000)

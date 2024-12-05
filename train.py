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
action_dim = 24  # Action space size (e.g., number of cards in hand) TODO
ppo = PPO(state_dim=state_dim, action_dim=action_dim)  # Your PPO model
ppo_strategy = PPOStrategy(ppo)

# Initialize Players
player1 = Player(0, ppo_strategy, "PPO_Player")
player2 = Player(1, RandomStrategy(), "Rand1_partner")
player3 = Player(2, RandomStrategy(), "Rand2_opp")
player4 = Player(3, RandomStrategy(), "Rand3_opp")

# Set up teams
team1 = Team(player1, player2, "Team1")
team2 = Team(player3, player4, "Team2")

# Initialize the game
game = Euchre(team1, team2)

def train_ppo(ppo, game, num_games=1000):
    for game_num in range(num_games):
        print(f"Starting game {game_num + 1}")
        
        # Initialize game
        state = game.playNewHand()  # Adjust if `playNewHand()` doesn't return a state
        done = False
        memory = []

        while not done:
            # PPO Player takes an action
            action_probs = ppo.predict_action(state)
            action = ppo.sample_action(action_probs)

            # Execute the action and observe the result
            next_state, reward, done = game.step(action)  # Replace with your step function

            # Store experience for PPO training
            memory.append((state, action, reward, next_state, action_probs[action]))
            state = next_state

        # After the game, update PPO with collected memory
        ppo.update(memory)

        # Optional: Save the model periodically
        if (game_num + 1) % 100 == 0:
            torch.save(ppo.actor.state_dict(), f"ppo_actor_{game_num + 1}.pth")
            torch.save(ppo.critic.state_dict(), f"ppo_critic_{game_num + 1}.pth")
            print(f"Model saved at game {game_num + 1}.")

# Train the model
train_ppo(ppo, game, num_games=1000)

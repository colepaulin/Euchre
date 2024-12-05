from Player import Player
from Team import Team
from RandomStrategy import RandomStrategy
from PPOStrategy import PPOStrategy
from Euchre import Euchre
from PPO import PPO
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# Initialize PPO Strategy
state_dim = 633  # State vector size
action_dim = 19  # Action space size (e.g., number of cards in hand)
ppo: PPO = PPO(state_dim=state_dim, action_dim=action_dim)  # Your PPO model

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
    actor_losses = []
    critic_losses = []
    total_rewards = []
    for game_num in range(num_games):
        print(f"Starting game {game_num + 1}")
        
        # Initialize game
        game = initializeNewEuchre(ppo)
        total_reward = 0
        game.playEuchre()
        total_reward = ppo.totalReward
        # After the game, update PPO with collected memory
        actor_loss, critic_loss = ppo.update()

        # Log metrics
        actor_losses.append(actor_loss)
        critic_losses.append(critic_loss)
        total_rewards.append(total_reward)

        # Optional: Save the model periodically
        if (game_num + 1) % 100 == 0:
            torch.save(ppo.actor.state_dict(), f"ppo_actor_{game_num + 1}.pth")
            torch.save(ppo.critic.state_dict(), f"ppo_critic_{game_num + 1}.pth")
            print(f"Model saved at game {game_num + 1}.")
        
        plot_training_progress(actor_losses, critic_losses, total_rewards)

# Train the model
train_ppo(ppo, num_games=1000)


def plot_training_progress(actor_losses, critic_losses, total_rewards):
    """Plot training progress for actor/critic losses and rewards."""
    plt.figure(figsize=(12, 4))

    # Actor loss
    plt.subplot(1, 3, 1)
    plt.plot(actor_losses, label="Actor Loss")
    plt.xlabel("Training Iteration")
    plt.ylabel("Loss")
    plt.title("Actor Loss Progress")
    plt.legend()

    # Critic loss
    plt.subplot(1, 3, 2)
    plt.plot(critic_losses, label="Critic Loss")
    plt.xlabel("Training Iteration")
    plt.ylabel("Loss")
    plt.title("Critic Loss Progress")
    plt.legend()

    # Total rewards
    plt.subplot(1, 3, 3)
    plt.plot(total_rewards, label="Total Rewards")
    plt.xlabel("Game Number")
    plt.ylabel("Total Rewards")
    plt.title("Reward Progress")
    plt.legend()

    plt.tight_layout()
    plt.show()
from Player import Player
from Team import Team
from RandomStrategy import RandomStrategy
from PPOStrategy import PPOStrategy
from GreedyStrategy import GreedyStrategy
from Euchre import Euchre
from PPO import PPO
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# Initialize PPO Strategy
state_dim = 633  # State vector size
action_dim = 20  # Action space size (e.g., number of cards in hand)
ppo: PPO = PPO(state_dim=state_dim, action_dim=action_dim, lr=1e-4)  # Your PPO model

def plot_training_progress(actor_losses, critic_losses, total_rewards, wins, losses):
    """Plot training progress for actor/critic losses, rewards, and win/loss counts."""
    plt.figure(figsize=(15, 8))

    # Actor loss
    plt.subplot(2, 2, 1)
    plt.plot(actor_losses, label="Actor Loss")
    plt.xlabel("Game Number")
    plt.ylabel("Loss")
    plt.title("Actor Loss Progress")
    plt.legend()

    # Critic loss
    plt.subplot(2, 2, 2)
    plt.plot(critic_losses, label="Critic Loss")
    plt.xlabel("Game Number")
    plt.ylabel("Loss")
    plt.title("Critic Loss Progress")
    plt.legend()

    # Total rewards
    plt.subplot(2, 2, 3)
    plt.plot(total_rewards, label="Total Rewards")
    plt.xlabel("Game Number")
    plt.ylabel("Rewards")
    plt.title("Reward Progress")
    plt.legend()

    # Wins and losses
    plt.subplot(2, 2, 4)
    plt.plot(wins, label="Wins", color="green")
    plt.plot(losses, label="Losses", color="red")
    plt.xlabel("Game Number")
    plt.ylabel("Count")
    plt.title("Wins and Losses Over Time")
    plt.legend()

    plt.tight_layout()
    
    # Save the plot as an image
    plt.savefig("training_progress.png")

    plt.show()

def initializeNewEuchre(ppo):
    # Initialize Players
    player1 = Player(0, PPOStrategy(ppo), "PPO_Player")
    player2 = Player(1, GreedyStrategy(), "Rand1_partner")
    player3 = Player(2, GreedyStrategy(), "Rand2_opp")
    player4 = Player(3, GreedyStrategy(), "Rand3_opp")

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
    wins = []
    losses = []
    win_count = 0
    loss_count = 0

    for game_num in range(num_games):
        print(f"Starting game {game_num + 1}")
        
        # Initialize game
        game = initializeNewEuchre(ppo)
        total_reward = 0
        winner = game.playEuchre()

        # Check if PPO player won or lost
        if winner.p1.id == 0 or winner.p2.id == 0:  # PPO player wins
            ppo.totalReward += 100
            ppo.memory[-1] = (ppo.memory[-1][0], ppo.memory[-1][1], ppo.memory[-1][2] + 100, ppo.memory[-1][3], ppo.memory[-1][4], 1)
            win_count += 1
        else:  # PPO player loses
            ppo.totalReward -= 100
            ppo.memory[-1] = (ppo.memory[-1][0], ppo.memory[-1][1], ppo.memory[-1][2] - 100, ppo.memory[-1][3], ppo.memory[-1][4], 1)
            loss_count += 1

        total_reward = ppo.totalReward

        # Update PPO model after the game
        actor_loss, critic_loss = ppo.update()

        # Log metrics
        actor_losses.append(actor_loss)
        critic_losses.append(critic_loss)
        total_rewards.append(total_reward)
        wins.append(win_count)
        losses.append(loss_count)

        # Optional: Save the model periodically
        if (game_num + 1) % 100 == 0:
            torch.save(ppo.actor.state_dict(), f"ppo_actor_{game_num + 1}.pth")
            torch.save(ppo.critic.state_dict(), f"ppo_critic_{game_num + 1}.pth")
            print(f"Model saved at game {game_num + 1}.")

    return (actor_losses, critic_losses, total_rewards, wins, losses)

# Train the model
(actor_losses, critic_losses, total_rewards, wins, losses) = train_ppo(ppo, num_games=10000)
plot_training_progress(actor_losses, critic_losses, total_rewards, wins, losses)
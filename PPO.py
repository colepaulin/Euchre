import torch
import torch.nn as nn
import numpy as np

# Define the PPO model
class PPO:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, eps_clip=0.2):
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.memory = [] # Added
        self.recentAction = None
        self.recentActionProb = None
        self.state = None
        self.nextState = None
        self.reward = None

        # Actor Network
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Softmax(dim=-1)
        )

        # Critic Network
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )

        # Optimizers
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=lr)

    def updateMemory(self):
        self.memory.append((self.state, 
                            self.recentAction, 
                            self.reward, 
                            self.nextState, 
                            self.recentActionProb))

    def predict_action(self, state):
        """Predict action probabilities."""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Convert state to tensor
        action_probs = self.actor(state_tensor).detach().numpy().flatten()
        return action_probs

    def compute_advantage(self, rewards, values):
        """Compute advantages and returns."""
        returns = []
        discounted_sum = 0
        for reward in reversed(rewards):
            discounted_sum = reward + self.gamma * discounted_sum
            returns.insert(0, discounted_sum)
        returns = np.array(returns)
        advantages = returns - np.array(values)
        return advantages, returns

    def update(self):
        """Update the actor and critic networks using PPO."""
        states, actions, rewards, next_states, old_action_probs = zip(*self.memory)

        # Convert to tensors
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        old_action_probs = torch.FloatTensor(old_action_probs)

        # Compute value predictions
        values = self.critic(states).squeeze(-1).detach().numpy()

        # Compute advantages and returns
        advantages, returns = self.compute_advantage(rewards, values)

        # Update actor network
        for _ in range(10):  # Number of epochs
            action_probs = self.actor(states).gather(1, actions.unsqueeze(1)).squeeze(1)
            ratios = action_probs / old_action_probs

            # Clip the objective
            clipped_ratios = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip)
            actor_loss = -torch.min(ratios * advantages, clipped_ratios * advantages).mean()

            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()

        # Update critic network
        values = self.critic(states).squeeze(-1)
        critic_loss = ((values - torch.FloatTensor(returns)) ** 2).mean()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

    def sample_action(self, action_probs):
        """Sample an action based on the predicted probabilities."""
        
        return np.random.choice(len(action_probs), p=action_probs)

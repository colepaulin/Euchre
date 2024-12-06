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
        self.reward = 0
        self.totalReward = 0

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
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
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
        action_probs = self.actor(state_tensor).detach().cpu().numpy().flatten()
        return action_probs

    def compute_advantage(self, rewards, values):
      """Compute advantages and returns."""
      returns = []
      discounted_sum = 0
      for reward in reversed(rewards):
          discounted_sum = reward + self.gamma * discounted_sum
          returns.insert(0, discounted_sum)
      
      returns = torch.FloatTensor(returns)  # Ensure returns is a PyTorch tensor
      advantages = returns - values  # Subtract PyTorch tensor `values`
      return advantages, returns

    def update(self):
        """Update the actor and critic networks using PPO and return losses."""
        states, actions, rewards, next_states, old_action_probs = zip(*self.memory)
        # Convert to tensors
        states = torch.FloatTensor(states[1:])
        actions = torch.LongTensor(actions[1:])
        rewards = torch.FloatTensor(rewards[1:])
        old_action_probs = torch.FloatTensor(old_action_probs[1:])
        
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)

        # Compute value predictions
        values = self.critic(states).squeeze(-1).detach().numpy()

        # Compute advantages and returns
        advantages, returns = self.compute_advantage(rewards, values)

        # Update actor network
        actor_losses = []
        for _ in range(10):  # Number of epochs
            action_probs = self.actor(states).gather(1, actions.unsqueeze(1)).squeeze(1)
            ratios = action_probs / old_action_probs

            # Clip the objective
            clipped_ratios = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip)
            actor_loss = -torch.min(ratios * advantages, clipped_ratios * advantages).mean()

            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()

            # Append the detached loss
            actor_losses.append(actor_loss.detach().item())

        # Update critic network
        values = self.critic(states).squeeze(-1)
        critic_loss = ((values - torch.FloatTensor(returns)) ** 2).mean()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        self.memory = []
        self.totalReward = 0

        # Return the average actor loss and critic loss
        return np.mean(actor_losses), critic_loss.item()

    def sample_action(self, action_probs):
      """Sample an action based on the predicted log-probabilities."""
      eps = 0.1  # Small epsilon to prevent zero probabilities

      # Add epsilon to all non-zero probabilities
      newActionProbs = action_probs + eps * action_probs

      # Normalize the probabilities to sum to 1
      total_prob = np.sum(newActionProbs)
      if total_prob == 0:
          raise ValueError("All action probabilities are zero after masking. Check your masking logic.")
      
      normalized_probs = newActionProbs / total_prob

      # Sample an action using the normalized probabilities
      try:
          return np.random.choice(len(normalized_probs), p=normalized_probs)
      except ValueError as e:
          print("Error sampling action:", e)
          print("action_probs:", action_probs)
          print("newActionProbs:", newActionProbs)
          print("Normalized probabilities:", normalized_probs)
          return None

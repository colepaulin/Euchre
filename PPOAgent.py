import torch

'''
TOO BE USED AS A MODEL FOR REFERENCE. WE ALREADY HAVE A PPOStrategy that
can be used by a generic Agent/Player, but it is nice to see how normal
pytorch implementations would have done it
'''

class PPOAgent:
    def __init__(self, model, optimizer, action_dim, gamma=0.99, clip_epsilon=0.2):
        self.model = model
        self.optimizer = optimizer
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon
        self.action_dim = action_dim
    
    def compute_advantages(self, rewards, values, dones):
        advantages = []
        advantage = 0
        for t in reversed(range(len(rewards))):
            delta = rewards[t] + self.gamma * (1 - dones[t]) * values[t + 1] - values[t]
            advantage = delta + self.gamma * (1 - dones[t]) * advantage
            advantages.insert(0, advantage)
        return advantages

    def update(self, states, actions, log_probs, rewards, dones):
        states = torch.stack(states)
        actions = torch.tensor(actions)
        old_log_probs = torch.tensor(log_probs)
        rewards = torch.tensor(rewards)
        dones = torch.tensor(dones)

        # Compute value predictions
        _, values = self.model(states)
        values = values.squeeze()

        # Compute advantages
        advantages = self.compute_advantages(rewards, values.detach(), dones)

        # PPO Update Loop
        for _ in range(4):  # Update multiple times per batch
            logits, new_values = self.model(states)
            new_log_probs = torch.log_softmax(logits, dim=-1)[range(len(actions)), actions]

            # Compute policy ratio
            ratio = torch.exp(new_log_probs - old_log_probs)

            # Clip the policy objective
            clip_advantages = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
            policy_loss = -torch.min(ratio * advantages, clip_advantages).mean()

            # Value loss
            value_loss = ((rewards + self.gamma * (1 - dones) * values[1:] - values[:-1]) ** 2).mean()

            # Total loss
            loss = policy_loss + 0.5 * value_loss

            # Backpropagation
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
import torch
import torch.nn as nn

class EuchrePPOModel(nn.Module):
    def __init__(self, input_dim, action_dim):
        super(EuchrePPOModel, self).__init__()
        
        # Shared layers
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        
        # Policy head (outputs action probabilities)
        self.policy_head = nn.Linear(128, action_dim)
        
        # Value head (outputs state value)
        self.value_head = nn.Linear(128, 1)
        
    def forward(self, x, action_mask=None):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        
        # Policy and value outputs
        policy_logits = self.policy_head(x)
        value = self.value_head(x)

        # TODO: figure out action masking
        if action_mask is not None:
            policy_logits = policy_logits + (action_mask.log() * 1e6)  # Large negative value for invalid actions


        return policy_logits, value
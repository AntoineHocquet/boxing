# src/agents/boxer.py

"""
Neural network player logic.
Boxer is the base class for players in the boxing game.
It stores
- position (2D vector)
- velocity (2D vector)
- energy
- a decision method (decide_action); now uses a PyTorch model.
"""

import numpy as np
import torch
import torch.nn as nn
    
class BoxerNet(nn.Module):
    """
    Simple MLP with shared hidden backbone.
    Outputs:
    - bounded 2D acceleration via Tanh
    - discrete action toggle (0 = move, 1 = attack)
    """
    def __init__(self, input_dim=4, hidden_dim=32):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU()
        )
        self.mean_head = nn.Sequential(
            nn.Linear(hidden_dim, 2),
            nn.Tanh()
        )
        self.log_std = nn.Parameter(torch.zeros(2))

        self.toggle_head = nn.Linear(hidden_dim, 2)  # logits for "move" and "attack"

    def forward(self, obs):
        x = self.backbone(obs)
        mean = self.mean_head(x)
        std = torch.exp(self.log_std)
        toggle_logits = self.toggle_head(x)
        return mean, std, toggle_logits


class Boxer:
    """
    A player in the boxing game.
    """
    def __init__(self, name, init_pos, init_energy=100.0, model=None):
        self.name = name
        self.position = np.array(init_pos, dtype=np.float32)  # 2D
        self.velocity = np.zeros(2, dtype=np.float32)
        self.energy = init_energy

        # Neural network controlling this agent
        self.model = model if model else BoxerNet()

        # Boxer action toggle
        self.mode = "move"  # "move" or "attack"

        # Parameters to tweak
        self.max_speed = 5.0
        self.accel_cost = 0.1
        self.hit_cost = 5.0
        self.damage_taken = 20.0

    def decide_action(self, obs, training=False, return_logprob=False):
        """
        Decide an action using the neural network.
        Returns:
        - action: 2D acceleration
        - logprob (optional): log probability of the action
        """
        obs_tensor = torch.tensor(obs, dtype=torch.float32)
        mean, std, toggle_logits = self.model(obs_tensor)

        dist = torch.distributions.Normal(mean, std)
        toggle_dist = torch.distributions.Categorical(logits=toggle_logits)

        if training:
            # enables backprop through sampling
            accel = dist.rsample()
            toggle = toggle_dist.sample()

            self.mode = "move" if toggle.item() == 0 else "attack"
            
            if return_logprob:
                logprob_accel = dist.log_prob(accel).sum()
                logprob_toggle = toggle_dist.log_prob(toggle)
                
                return accel, logprob_accel + logprob_toggle
            return accel
        else:
            # deterministic during inference
            self.mode = "move" if toggle_logits.argmax().item() == 0 else "attack"
            return mean.detach().numpy()

    def apply_acceleration(self, accel, dt):
        """
        Apply acceleration to velocity.
        """
        if self.mode != "move":
            return  # Do nothing

        # accel is a 2D vector
        if isinstance(accel, torch.Tensor):
            accel_np = accel.detach().numpy()
        else:
            accel_np = accel

        cost = self.accel_cost * np.linalg.norm(accel_np)
        self.energy -= cost
        self.velocity += accel_np * dt
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

    def try_hit(self, opponent):
        """
        Try to hit the opponent. If close enough, causes damage.
        """
        if self.mode != "attack":
            return False

        dist = np.linalg.norm(self.position - opponent.position)
        if dist < 1.0:
            opponent.energy -= self.damage_taken
            self.energy -= self.hit_cost
            return True
        return False

    def is_alive(self):
        """
        Tells whether the boxer is KO (False) or not (True). 
        """
        return self.energy > 0
    
    def reset(self, init_pos, init_energy=100.0):
        """
        Resets the dynamic state of the boxer for a new fight.
        """
        self.position = np.array(init_pos, dtype=np.float32)
        self.velocity = np.zeros(2, dtype=np.float32)
        self.energy = init_energy
        self.mode = "move"

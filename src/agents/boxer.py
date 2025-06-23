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
    Simple MLP taking a 4D obs (relative pos + velocity).
    Outputs a bounded 2D acceleration via Tanh().
    """
    def __init__(self, input_dim=4, hidden_dim=32):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2),  # Output: 2D acceleration
            nn.Tanh()  # Bound acceleration between -1 and 1
        )

    def forward(self, obs):
        return self.model(obs)


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

        # Parameters to tweak
        self.max_speed = 5.0
        self.accel_cost = 0.1
        self.hit_cost = 5.0
        self.damage_taken = 20.0

    def decide_action(self, obs, training=False):
        """
        Predicts acceleration from observation.
        If training=True, returns a tensor with gradient tracking.
        """
        # if model is None, take random action
        if self.model is None:
            return np.random.uniform(-1.0, 1.0, 2)

        # otherwise, use model
        obs_tensor = torch.tensor(obs, dtype=torch.float32)
        if training:
            accel = self.model(obs_tensor)
        else:
            with torch.no_grad():
                accel = self.model(obs_tensor)
        return accel.numpy() if not training else accel

    def apply_acceleration(self, accel, dt):
        cost = self.accel_cost * np.linalg.norm(accel)
        self.energy -= cost
        self.velocity += accel * dt
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

    def try_hit(self, opponent):
        """
        Try to hit the opponent. If close enough, causes damage.
        """
        dist = np.linalg.norm(self.position - opponent.position)
        if dist < 1.0:
            opponent.energy -= self.damage_taken
            self.energy -= self.hit_cost

    def is_alive(self):
        return self.energy > 0

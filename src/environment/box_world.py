# src/environment/box_world.py
"""
2D box environment.
This defines:
- A square 2D world of size x size
- position updates with time step dt
- reflection at walls (bounce back)
"""
import numpy as np

class BoxWorld:
    """
    Basic 2D box environment.
    The box is a square with walls at 0 and size.
    The box is centered at (size/2, size/2).
    """
    def __init__(self, size=10.0):
        """
        A simple 2D square box world with walls at 0 and size.
        """
        self.size = size

    def clip_position(self, position):
        """
        Ensure the player stays inside the box.
        """
        return np.clip(position, 0, self.size)

    def reflect_if_hit_wall(self, position, velocity):
        """
        Reflects the velocity if the agent hits a wall.
        """
        for i in range(2):  # x and y
            if position[i] <= 0 or position[i] >= self.size:
                velocity[i] *= -1  # bounce back
        return velocity

    def update_position(self, position, velocity, dt=0.1):
        """
        Moves the agent with given velocity and time step.
        """
        new_pos = position + velocity * dt
        new_pos = self.clip_position(new_pos)
        return new_pos

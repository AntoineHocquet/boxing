# src/environment/fight.py
"""
Fight simulation logic.
This is the core fight loop: it
- simulates time progression until one boxer is KO or time is up.
- handles movement, wall collisions, actions, and hits.
- returns a detailed fight log for later use (e.g., animation or training signals).
"""

from src.environment.box_world import BoxWorld
from src.agents.boxer import Boxer
import numpy as np


def run_fight(boxer_a, boxer_b, T=10.0, dt=0.1, box_size=10.0, track_obs=False):
    world = BoxWorld(size=box_size)
    t = 0.0
    log = []

    while t < T and boxer_a.is_alive() and boxer_b.is_alive():
        obs_a = get_observation(boxer_a, boxer_b, box_size)
        obs_b = get_observation(boxer_b, boxer_a, box_size)

        a_accel = boxer_a.decide_action(obs_a)
        b_accel = boxer_b.decide_action(obs_b)

        boxer_a.apply_acceleration(a_accel, dt)
        boxer_b.apply_acceleration(b_accel, dt)

        # Update velocities with wall reflection
        boxer_a.velocity = world.reflect_if_hit_wall(boxer_a.position, boxer_a.velocity)
        boxer_b.velocity = world.reflect_if_hit_wall(boxer_b.position, boxer_b.velocity)

        boxer_a.position = world.update_position(boxer_a.position, boxer_a.velocity, dt)
        boxer_b.position = world.update_position(boxer_b.position, boxer_b.velocity, dt)

        # Try to hit
        boxer_a.try_hit(boxer_b)
        boxer_b.try_hit(boxer_a)

        log_entry = {
            "t": float(t),
            "a_pos": [float(x) for x in boxer_a.position.tolist()],
            "b_pos": [float(x) for x in boxer_b.position.tolist()],
            "a_energy": float(boxer_a.energy),
            "b_energy": float(boxer_b.energy)
        }

        if track_obs:
            log_entry["a_obs"] = [float(x) for x in obs_a.tolist()]
            log_entry["b_obs"] = [float(x) for x in obs_b.tolist()]
            log_entry["a_action"] = [float(x) for x in a_accel.tolist()]
            log_entry["b_action"] = [float(x) for x in b_accel.tolist()]

        log.append(log_entry)

        t += dt

    winner = None
    if boxer_a.is_alive() and not boxer_b.is_alive():
        winner = "A"
    elif boxer_b.is_alive() and not boxer_a.is_alive():
        winner = "B"

    return {
        "log": log,
        "winner": winner,
        "final_energy": (float(boxer_a.energy), float(boxer_b.energy))
    }


def get_observation(self_boxer, opponent_boxer, box_size):
    """
    Return a simple observation for now: relative pos and velocity.
    Later, enrich with distances to walls, etc.
    """
    rel_pos = opponent_boxer.position - self_boxer.position
    rel_vel = opponent_boxer.velocity - self_boxer.velocity
    return np.concatenate([rel_pos, rel_vel])

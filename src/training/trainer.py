# src/training/trainer.py

"""
Training loop for adversarial learning.
Logics:
- Each model is updated with its full episode's worth of observations.
- The target is the win/loss reward, broadcast over all time steps.
- This gives a kind of Monte Carlo policy evaluation flavor — future versions could replace this with discounted returns, actor-critic, etc.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from src.agents.boxer import Boxer, BoxerNet
from src.environment.fight import run_fight
from src.utils.io import save_fight_log
import os


def train_agents(epochs=100, T=30, save_dir="models", boxer_a=None, boxer_b=None):
    """
    Train two boxers adversarially using observations from fights.
    Uses a simple regression loss toward +1 if won, 0 if lost.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Initialize boxers
    if boxer_a is None:
        model_a = BoxerNet()
        boxer_a = Boxer("A", init_pos=[2.0, 2.0], model=model_a)
    else:
        model_a = boxer_a.model

    if boxer_b is None:
        model_b = BoxerNet()
        boxer_b = Boxer("B", init_pos=[8.0, 8.0], model=model_b)
    else:
        model_b = boxer_b.model

    # Initialize optimizers
    optimizer_a = optim.Adam(model_a.parameters(), lr=1e-3)
    optimizer_b = optim.Adam(model_b.parameters(), lr=1e-3)

    # Training loop
    for epoch in range(1, epochs + 1):
        # refresh boxers for a new fight (reset energy, position & velocity)
        boxer_a.reset(init_pos=[2.0, 2.0])
        boxer_b.reset(init_pos=[8.0, 8.0])

        # Run a fight with observation tracking
        result = run_fight(boxer_a, boxer_b, T=T, dt=0.1, track_obs=True, training=True)
        log = result["log"]
        winner = result["winner"]

        # Compute rewards
        reward_a = 1.0 if winner == "A" else 0.0
        reward_b = 1.0 if winner == "B" else 0.0

        # Accumulate REINFORCE loss
        logprobs_a = [entry["a_logprob"] for entry in log]
        logprobs_b = [entry["b_logprob"] for entry in log]

        # Compute loss
        loss_a = -reward_a * torch.stack(logprobs_a).sum()
        loss_b = -reward_b * torch.stack(logprobs_b).sum()

        # Update models
        optimizer_a.zero_grad()
        loss_a.backward()
        optimizer_a.step()

        optimizer_b.zero_grad()
        loss_b.backward()
        optimizer_b.step()

        # Print progress
        print(f"Epoch {epoch:03d} | Winner: {winner} | Loss A: {loss_a.item():.4f} | Loss B: {loss_b.item():.4f}")

        # Save models and logs every 100 epochs
        if epoch % 100 == 0:
            torch.save(model_a.state_dict(), f"{save_dir}/model_a_epoch{epoch}.pt")
            torch.save(model_b.state_dict(), f"{save_dir}/model_b_epoch{epoch}.pt")
            save_fight_log(result, f"fights/log_epoch{epoch}.json")

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


def train_agents(epochs=100, save_dir="models"):
    """
    Train two boxers adversarially using observations from fights.
    Uses a simple regression loss toward +1 if won, 0 if lost.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Create two agents with their own models
    model_a = BoxerNet()
    model_b = BoxerNet()

    boxer_a = Boxer("A", init_pos=[2.0, 2.0], model=model_a)
    boxer_b = Boxer("B", init_pos=[8.0, 8.0], model=model_b)

    optimizer_a = optim.Adam(model_a.parameters(), lr=1e-3)
    optimizer_b = optim.Adam(model_b.parameters(), lr=1e-3)

    loss_fn = nn.MSELoss()

    for epoch in range(1, epochs + 1):
        # Run a fight with observation tracking
        result = run_fight(boxer_a, boxer_b, T=5.0, dt=0.1, track_obs=True)
        log = result["log"]
        winner = result["winner"]

        reward_a = 1.0 if winner == "A" else 0.0
        reward_b = 1.0 if winner == "B" else 0.0

        # Collect training examples from log
        obs_a_list = [torch.tensor(entry["a_obs"], dtype=torch.float32) for entry in log]
        obs_b_list = [torch.tensor(entry["b_obs"], dtype=torch.float32) for entry in log]

        target_a = torch.tensor([reward_a] * len(obs_a_list), dtype=torch.float32)
        target_b = torch.tensor([reward_b] * len(obs_b_list), dtype=torch.float32)

        # Train model A
        optimizer_a.zero_grad()
        preds_a = torch.stack([model_a(obs) for obs in obs_a_list])
        loss_a = loss_fn(preds_a.mean(dim=1), target_a)
        loss_a.backward()
        optimizer_a.step()

        # Train model B
        optimizer_b.zero_grad()
        preds_b = torch.stack([model_b(obs) for obs in obs_b_list])
        loss_b = loss_fn(preds_b.mean(dim=1), target_b)
        loss_b.backward()
        optimizer_b.step()

        print(f"Epoch {epoch:03d} | Winner: {winner} | Loss A: {loss_a.item():.4f} | Loss B: {loss_b.item():.4f}")

        # Save models and logs every 10 epochs
        if epoch % 10 == 0:
            torch.save(model_a.state_dict(), f"{save_dir}/model_a_epoch{epoch}.pt")
            torch.save(model_b.state_dict(), f"{save_dir}/model_b_epoch{epoch}.pt")
            save_fight_log(result, f"fights/log_epoch{epoch}.json")

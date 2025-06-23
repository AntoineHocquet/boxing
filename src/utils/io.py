# src/utils/io.py

""" 
Utility functions for saving/loading
"""

import json
import os
import torch
from src.agents.boxer import BoxerNet


def save_fight_log(log_data, filepath):
    """Save fight log to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(log_data, f, indent=2)


def load_fight_log(filepath):
    """Load fight log from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def load_models(path_a, path_b):
    """
    Load two models from file paths.
    Returns (model_a, model_b), both instances of BoxerNet with weights loaded.
    """
    model_a = BoxerNet()
    model_a.load_state_dict(torch.load(path_a))
    model_a.eval()

    model_b = BoxerNet()
    model_b.load_state_dict(torch.load(path_b))
    model_b.eval()

    return model_a, model_b

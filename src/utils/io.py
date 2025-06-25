# src/utils/io.py

""" 
Utility functions for saving/loading
"""

import json
import os
import re
import torch
from src.agents.boxer import BoxerNet


def save_fight_log(result, path):
    # Clean tensors before saving
    def clean(obj):
        if isinstance(obj, torch.Tensor):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean(x) for x in obj]
        else:
            return obj

    log_data = clean(result)
    with open(path, "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"✅ Fight log saved to {path}")


def load_fight_log(filepath):
    """Load fight log from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)

    print(f"✅ Fight log loaded from {filepath}")


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


def find_latest_model(path, prefix):
    """
    Find the latest model in a directory matching a given prefix.
    For example, prefix = 'model_a_epoch'
    """
    candidates = []
    for fname in os.listdir(path):
        if fname.startswith(prefix) and fname.endswith(".pt"):
            match = re.search(rf"{re.escape(prefix)}(\d+)\.pt", fname)
            if match:
                epoch = int(match.group(1))
                candidates.append((epoch, fname))
                print(f"Found latest {fname} with epoch {epoch}")
            
    if not candidates:
        raise FileNotFoundError(f"No matching models with prefix '{prefix}' in {path}")

    # Get the file with the max epoch
    latest_file = max(candidates, key=lambda x: x[0])[1]
    return os.path.join(path, latest_file)

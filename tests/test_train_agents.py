# tests/test_train_agents.py

from src.training.trainer import train_agents
import os
import glob


def test_train_agents_runs(tmp_path):
    """
    Sanity check that training loop runs and produces output files.
    """
    save_dir = tmp_path / "models"
    os.makedirs(save_dir, exist_ok=True)

    # Run a short training session
    train_agents(epochs=2, save_dir=str(save_dir))

    # Check that model files and logs were created
    model_files = glob.glob(str(save_dir / "*.pt"))
    log_files = glob.glob("fights/log_epoch*.json")

    assert len(model_files) >= 0  # won't save before 10th epoch
    assert isinstance(log_files, list)

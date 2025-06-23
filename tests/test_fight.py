# tests/test_fight.py

import pytest
import numpy as np
from src.agents.boxer import Boxer
from src.environment.fight import run_fight


def test_fight_simulation():
    boxer_a = Boxer("A", init_pos=[2.0, 2.0])
    boxer_b = Boxer("B", init_pos=[8.0, 8.0])

    result = run_fight(boxer_a, boxer_b, T=1.0, dt=0.1, box_size=10.0)
    log = result["log"]
    print(log)

    # Check log is not empty
    assert len(log) > 0

    for entry in log:
        a_pos = np.array(entry["a_pos"])
        b_pos = np.array(entry["b_pos"])

        # Check that positions stay inside the box
        assert np.all(a_pos >= 0) and np.all(a_pos <= 10)
        assert np.all(b_pos >= 0) and np.all(b_pos <= 10)

        # Check energy is positive
        assert entry["a_energy"] >= 0
        assert entry["b_energy"] >= 0

    # Winner must be None or 'A' or 'B'
    assert result["winner"] in [None, "A", "B"]

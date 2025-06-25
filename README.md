# Boxing: Neural Networks Trained to Fight

**Boxing** is a reinforcement learning and adversarial training project where two neural networks are trained to fight inside a 2D box. Each player (A and B) learns strategies through self-play and GAN-style parameter updates. Inspired by earlier MATLAB genetic algorithms, this Python implementation uses PyTorch and modern MLOps tooling.

---

## 🚀 Features

* Symmetric 2D boxing ring with walls and collisions
* Neural networks control agents' actions: acceleration and hitting
* Discrete time loop with KO or time limit condition
* Game dynamics based on energy, momentum, and position
* PyTorch-based training with adversarial learning
* CLI for training and running matches
* Fight animations with matplotlib

---

## 🧠 Neural Architecture

Each agent (A and B) is modeled by a neural network that receives environment variables:

* Relative position & velocity
* Wall proximity
* Current energy level

The networks output a choice of action (acceleration or hit) and direction.

At the end of each fight (episode), the winner's network is reinforced and the loser's updated adversarially.

---

## 🕹️ CLI Usage

Install with:

```bash
pip install -e .
```

Then use:

```bash
python boxing.py train --epochs 100
python boxing.py fight --render
```

---

## 🧪 Development Setup

Install requirements with:

```bash
pip install -r requirements.txt
```

Run tests with:

```bash
pytest
```

---

## 📁 Project Structure

```
.
├── animations/               # Generated fight GIFs
│   └── fight_.gif
├── boxing.py                # Main entry point
├── fights/                  # Fight logs
│   ├── log_epoch100.json
│   └── log.json
├── Makefile                 # Common development commands
├── models/                  # Saved model weights
│   ├── model_a_epoch100.pt
│   └── model_b_epoch100.pt
├── README.md
├── requirements.txt         # Runtime + development dependencies
├── setup.py                 # Packaging info
├── src/
│   ├── agents/
│   │   └── boxer.py         # Agent (neural network) logic
│   ├── cli.py               # Command-line interface
│   ├── environment/
│   │   ├── box_world.py     # 2D environment with wall logic
│   │   └── fight.py         # Fight mechanics
│   ├── training/
│   │   └── trainer.py       # Adversarial training logic
│   ├── utils/
│   │   ├── io.py            # I/O and logging utilities
│   │   └── visuals.py       # Plotting and animations
│   └── __init__.py
└── tests/                   # Unit tests for each module
    ├── test_core.py
    ├── test_fight.py
    ├── test_run_and_animate.py
    └── test_train_agents.py
```

---

## 📜 License

MIT License

---

## 🤝 Acknowledgements

Originally inspired by a MATLAB genetic simulation of fighters designed by the author. This project upgrades it with modern deep learning, GAN-like feedback, and a modular Pythonic architecture.

---

## 🛠️ Future Work

* Replace deterministic dynamics with stochasticity
* Add visual debugging with wall collisions
* Integrate logging and checkpoints
* Add tournament/batch evaluation
* Export fight GIFs and scores

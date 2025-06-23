# CLI entrypoint using argparse or click
# src/cli.py

import fire
from src.training.trainer import train_agents
from src.environment.fight import run_fight
from src.utils.io import load_models, save_fight_log
from src.utils.visuals import animate_fight

class BoxingFireCLI:
    def train(self, epochs=100, save_dir="models/"):
        return train_agents(epochs=epochs, save_dir=save_dir)

    def fight(self, model_a, model_b, save_log="fights/fight_log.json"):
        a, b = load_models(model_a, model_b)
        fight_log = run_fight(a, b)
        save_fight_log(fight_log, save_log)
        return fight_log

    def animate(self, log, out="animations/fight.gif"):
        return animate_fight(log_path=log, output_path=out)

if __name__ == "__main__":
    fire.Fire(BoxingFireCLI)

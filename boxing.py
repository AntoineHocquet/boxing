# boxing.py

"""
🤖 BOXING: Train and battle adversarial neural agents in a 2D ring!
"""

import argparse
from src.training.trainer import train_agents
from src.environment.fight import run_fight
from src.utils.io import load_models, save_fight_log, find_latest_model
from src.utils.visuals import animate_fight
from src.agents.boxer import Boxer
import os

def main():
    parser = argparse.ArgumentParser(description="🤖 BOXING: Train and battle adversarial neural agents in a 2D ring!")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Train
    train_parser = subparsers.add_parser("train", help="Train two agents")
    train_parser.add_argument("--epochs", type=int, default=100)
    train_parser.add_argument("--save-dir", type=str, default="models/")

    # Retrain
    retrain_parser = subparsers.add_parser("retrain", help="Retrain two agents")
    retrain_parser.add_argument("--model-a", required=False)
    retrain_parser.add_argument("--model-b", required=False)
    retrain_parser.add_argument("--epochs", type=int, default=100)
    retrain_parser.add_argument("--save-dir", type=str, default="models/")

    # Fight
    fight_parser = subparsers.add_parser("fight", help="Run a match between two agents")
    fight_parser.add_argument("--model-a", required=True)
    fight_parser.add_argument("--model-b", required=True)
    fight_parser.add_argument("--save-log", default="fights/fight_log.json")

    # Animate
    anim_parser = subparsers.add_parser("animate", help="Animate a fight log")
    anim_parser.add_argument("--log", required=True)
    anim_parser.add_argument("--out", default="")

    args = parser.parse_args()

    if args.command == "train":
        train_agents(epochs=args.epochs, save_dir=args.save_dir)

    elif args.command == "retrain":
        model_a_path = args.model_a or find_latest_model(args.save_dir, "model_a_epoch")
        model_b_path = args.model_b or find_latest_model(args.save_dir, "model_b_epoch")
        print(f"📂 Using models:\n  A: {model_a_path}\n  B: {model_b_path}")

        model_a, model_b = load_models(model_a_path, model_b_path)
        boxer_a = Boxer("A", init_pos=[2.0, 2.0], model=model_a)
        boxer_b = Boxer("B", init_pos=[8.0, 8.0], model=model_b)

        train_agents(epochs=args.epochs, save_dir=args.save_dir, boxer_a=boxer_a, boxer_b=boxer_b)


    elif args.command == "fight":
        model_a, model_b = load_models(args.model_a, args.model_b)
        boxer_a = Boxer("A", init_pos=[2.0, 2.0], model=model_a)
        boxer_b = Boxer("B", init_pos=[8.0, 8.0], model=model_b)
        result = run_fight(boxer_a, boxer_b, T=30.0, dt=0.1)
        save_fight_log(result, args.save_log)
        print(f"✅ Fight complete. Log saved to fights/log_epoch{args.save_log}.json")

    elif args.command == "animate":
        animate_fight(log_path=f"fights/log_epoch{args.log}.json", output_path=f"animations/fight_{args.out}.gif")
        print(f"🎞️ Animation saved to animations/fight_{args.out}.gif")

if __name__ == "__main__":
    main()


# def main():
#     parser = argparse.ArgumentParser(
#         description="🤖 BOXING: Train and battle adversarial neural agents in a 2D ring!"
#     )
#     subparsers = parser.add_subparsers(dest="command", required=True)

#     # Train command
#     train_parser = subparsers.add_parser("train", help="Train two agents adversarially")
#     train_parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
#     train_parser.add_argument("--save-dir", type=str, default="models/", help="Directory to save models")

#     # Fight command
#     fight_parser = subparsers.add_parser("fight", help="Run a match between two trained agents")
#     fight_parser.add_argument("--model-a", type=str, required=True, help="Path to model A")
#     fight_parser.add_argument("--model-b", type=str, required=True, help="Path to model B")
#     fight_parser.add_argument("--save-log", type=str, default="fights/fight_log.json", help="Where to save fight log")

#     # Animate command
#     anim_parser = subparsers.add_parser("animate", help="Animate a fight log")
#     anim_parser.add_argument("--log", type=str, required=True, help="Path to saved fight log (.json)")
#     anim_parser.add_argument("--out", type=str, default="animations/fight.gif", help="Output GIF path")

#     # Parse arguments and dispatch
#     args = parser.parse_args()

#     if args.command == "train":
#         train_agents(epochs=args.epochs, save_dir=args.save_dir)

#     elif args.command == "fight":
#         model_a, model_b = load_models(args.model_a, args.model_b)
#         fight_log = run_fight(model_a, model_b)
#         save_fight_log(fight_log, args.save_log)

#     elif args.command == "animate":
#         animate_fight(log_path=args.log, output_path=args.out)

# boxing.py

import argparse
from src.training.trainer import train_agents
from src.environment.fight import run_fight
from src.utils.io import load_models, save_fight_log
from src.utils.visuals import animate_fight
from src.agents.boxer import Boxer
import os

def main():
    parser = argparse.ArgumentParser(description="🤖 BOXING CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Train
    train_parser = subparsers.add_parser("train", help="Train two agents")
    train_parser.add_argument("--epochs", type=int, default=100)
    train_parser.add_argument("--save-dir", type=str, default="models/")

    # Fight
    fight_parser = subparsers.add_parser("fight", help="Run a match between two agents")
    fight_parser.add_argument("--model-a", required=True)
    fight_parser.add_argument("--model-b", required=True)
    fight_parser.add_argument("--save-log", default="fights/fight_log.json")

    # Animate
    anim_parser = subparsers.add_parser("animate", help="Animate a fight log")
    anim_parser.add_argument("--log", required=True)
    anim_parser.add_argument("--out", default="animations/fight.gif")

    args = parser.parse_args()

    if args.command == "train":
        train_agents(epochs=args.epochs, save_dir=args.save_dir)

    elif args.command == "fight":
        model_a, model_b = load_models(args.model_a, args.model_b)
        boxer_a = Boxer("A", init_pos=[2.0, 2.0], model=model_a)
        boxer_b = Boxer("B", init_pos=[8.0, 8.0], model=model_b)
        result = run_fight(boxer_a, boxer_b, T=5.0, dt=0.1)
        save_fight_log(result, args.save_log)
        print(f"✅ Fight complete. Log saved to {args.save_log}")

    elif args.command == "animate":
        animate_fight(log_path=args.log, output_path=args.out)
        print(f"🎞️ Animation saved to {args.out}")

if __name__ == "__main__":
    main()


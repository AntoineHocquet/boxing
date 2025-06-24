# tests/test_run_and_animate.py

from src.agents.boxer import Boxer
from src.environment.fight import run_fight
from src.utils.io import save_fight_log
from src.utils.visuals import animate_fight

# Step 1: Create boxers
boxer_a = Boxer("A", init_pos=[2.0, 2.0])
boxer_b = Boxer("B", init_pos=[8.0, 8.0])

# Step 2: Run the fight
result = run_fight(boxer_a, boxer_b, T=15.0, dt=0.1)

# Step 3: Save the log
save_fight_log(result, "fights/log.json")

# Step 4: Generate animation
animate_fight("fights/log.json", "animations/fight.gif")

print("✅ Fight complete and animation saved to animations/fight.gif")

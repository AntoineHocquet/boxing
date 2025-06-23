# src/utils/visuals.py

import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def animate_fight(log_path, output_path):
    with open(log_path, "r") as f:
        fight_data = json.load(f)

    log = fight_data.get("log", [])
    if len(log) == 0:
        print("❌ Fight log is empty. Cannot animate.")
        return

    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.set_title("Boxing Match")

    a_dot, = ax.plot([], [], 'ro', label='A')
    b_dot, = ax.plot([], [], 'bo', label='B')
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    energy_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
    ax.legend()

    def init():
        a_dot.set_data([], [])
        b_dot.set_data([], [])
        time_text.set_text('')
        energy_text.set_text('')
        return a_dot, b_dot, time_text, energy_text

    def update(frame):
        entry = log[frame]
        a_pos = entry.get("a_pos", [None, None])
        b_pos = entry.get("b_pos", [None, None])

        try:
            a_dot.set_data([a_pos[0]], [a_pos[1]])
            b_dot.set_data([b_pos[0]], [b_pos[1]])
            time_text.set_text(f"t = {entry['t']:.1f}s")
            energy_text.set_text(f"E_A = {entry['a_energy']:.1f} | E_B = {entry['b_energy']:.1f}")
            return a_dot, b_dot, time_text, energy_text
        except Exception as e:
            print(f"⚠️ Skipping frame {frame} due to error: {e}")
            return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(log), init_func=init, blit=False, interval=100
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ani.save(output_path, writer='pillow', dpi=100)
    plt.close(fig)

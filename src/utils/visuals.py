# src/utils/visuals.py

import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import os

def animate_fight(log_path, output_path):
    with open(log_path, "r") as f:
        fight_data = json.load(f)

    log = fight_data.get("log", [])
    if len(log) == 0:
        print("❌ Fight log is empty. Cannot animate.")
        return

    # Extend log to repeat the final KO frame several times for visibility
    extended_log = log + [log[-1]] * 10 if log else log

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.set_title("Boxing Match")

    box_frame = patches.Rectangle((0, 0), 10, 10, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(box_frame)

    a_dot, = ax.plot([], [], 'ro', label='A', markersize=12)
    b_dot, = ax.plot([], [], 'bo', label='B', markersize=12)
    hit_line, = ax.plot([], [], 'k-', lw=2, alpha=0.0)

    ax.legend(loc='upper left')

    a_energy_bar = patches.Rectangle((10.5, 6.0), 0.3, 3.0, color='red')
    b_energy_bar = patches.Rectangle((11.3, 6.0), 0.3, 3.0, color='blue')
    ax.add_patch(a_energy_bar)
    ax.add_patch(b_energy_bar)

    a_energy_label = ax.text(10.65, 9.2, "E_A", fontsize=9, color='red', ha='center')
    b_energy_label = ax.text(11.45, 9.2, "E_B", fontsize=9, color='blue', ha='center')
    time_text = ax.text(10.5, 1.2, '', fontsize=10, color='black', ha='left')
    a_hit_text = ax.text(10.5, 0.8, 'Hits A: 0', fontsize=9, color='red', ha='left')
    b_hit_text = ax.text(10.5, 0.5, 'Hits B: 0', fontsize=9, color='blue', ha='left')
    ko_text = ax.text(5, 5, '', fontsize=18, color='black', ha='center', va='center')

    hit_count_a = 0
    hit_count_b = 0
    last_ko_frame = -1

    def init():
        a_dot.set_data([], [])
        b_dot.set_data([], [])
        hit_line.set_data([], [])
        hit_line.set_alpha(0.0)
        a_energy_bar.set_height(3.0)
        b_energy_bar.set_height(3.0)
        time_text.set_text('')
        a_hit_text.set_text('Hits A: 0')
        b_hit_text.set_text('Hits B: 0')
        ko_text.set_text('')
        return a_dot, b_dot, hit_line, time_text, a_energy_bar, b_energy_bar, a_energy_label, b_energy_label, a_hit_text, b_hit_text, ko_text

    def update(frame):
        nonlocal hit_count_a, hit_count_b, last_ko_frame
        entry = extended_log[frame]
        a_pos = entry.get("a_pos", [None, None])
        b_pos = entry.get("b_pos", [None, None])

        try:
            a_dot.set_data([a_pos[0]], [a_pos[1]])
            b_dot.set_data([b_pos[0]], [b_pos[1]])
            time_text.set_text(f"t = {entry['t']:.1f}s")

            if entry.get("a_hit", False):
                hit_line.set_data([a_pos[0], b_pos[0]], [a_pos[1], b_pos[1]])
                hit_line.set_color('red')
                hit_line.set_alpha(1.0)
                hit_count_a += 1
            elif entry.get("b_hit", False):
                hit_line.set_data([b_pos[0], a_pos[0]], [b_pos[1], a_pos[1]])
                hit_line.set_color('blue')
                hit_line.set_alpha(1.0)
                hit_count_b += 1
            else:
                hit_line.set_alpha(0.0)

            a_hit_text.set_text(f"Hits A: {hit_count_a}")
            b_hit_text.set_text(f"Hits B: {hit_count_b}")

            if entry['a_energy'] <= 0:
                ko_text.set_text("KO! B wins")
                ko_text.set_color('blue')
                last_ko_frame = frame
            elif entry['b_energy'] <= 0:
                ko_text.set_text("KO! A wins")
                ko_text.set_color('red')
                last_ko_frame = frame
            elif last_ko_frame >= 0 and frame - last_ko_frame <= 5:
                pass
            else:
                ko_text.set_text('')

            a_energy = max(0.0, min(entry['a_energy'], 100.0))
            b_energy = max(0.0, min(entry['b_energy'], 100.0))
            a_energy_bar.set_height(3.0 * (a_energy / 100.0))
            b_energy_bar.set_height(3.0 * (b_energy / 100.0))

            return a_dot, b_dot, hit_line, time_text, a_energy_bar, b_energy_bar, a_energy_label, b_energy_label, a_hit_text, b_hit_text, ko_text
        except Exception as e:
            print(f"⚠️ Skipping frame {frame} due to error: {e}")
            return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(extended_log), init_func=init, blit=False, interval=100
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ani.save(output_path, writer='pillow', dpi=100)
    plt.close(fig)

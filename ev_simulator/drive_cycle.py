"""
Synthetic driving cycle generator.

Real EV homologation cycles (WLTP, IDC) are licensed datasets. For a
student/portfolio project, we generate a representative stop-and-go
urban profile with randomized accel/cruise/decel/idle phases, which
captures the same qualitative stress pattern (frequent acceleration,
low average speed, lots of braking events) that matters for range and
regen analysis.
"""
import numpy as np


def generate_indian_urban_cycle(duration_s=1200, dt_s=1.0, max_speed_kmph=50, seed=42):
    """
    Returns (time_array_s, speed_array_mps).

    Models Indian city driving: frequent stops, moderate top speed,
    lots of acceleration/deceleration events relative to cruise time.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0, duration_s, dt_s)
    speed = np.zeros_like(t, dtype=float)
    max_speed_mps = max_speed_kmph / 3.6

    i = 0
    current_speed = 0.0
    while i < len(t):
        phase = rng.choice(["accel", "cruise", "decel", "idle"], p=[0.30, 0.30, 0.25, 0.15])
        phase_len = int(rng.integers(5, 40))
        for _ in range(phase_len):
            if i >= len(t):
                break
            if phase == "accel":
                current_speed = min(max_speed_mps, current_speed + rng.uniform(0.3, 1.2))
            elif phase == "cruise":
                current_speed = max(0.0, min(max_speed_mps, current_speed + rng.normal(0, 0.05)))
            elif phase == "decel":
                current_speed = max(0.0, current_speed - rng.uniform(0.3, 1.5))
            else:  # idle
                current_speed = 0.0
            speed[i] = current_speed
            i += 1
    return t, speed
